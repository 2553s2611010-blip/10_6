
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
import streamlit as st
from bs4 import BeautifulSoup

# -----------------------------
# 기본 설정
# -----------------------------
SCHOOL_NAME = "천안오성고등학교"
HOME_URL = "https://ohsung.caehs.kr"

st.set_page_config(
    page_title="오성 공지 알리미",
    page_icon="📣",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #f5f7fb;
    }
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #173b70;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #63718a;
        margin-bottom: 1.3rem;
    }
    .notice-card {
        padding: 18px;
        background: white;
        border: 1px solid #e1e7f0;
        border-radius: 13px;
        margin-bottom: 12px;
    }
    .notice-date {
        color: #718096;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}

BOARD_KEYWORDS = (
    "공지사항",
    "공지",
    "가정통신문",
    "학교소식",
    "알림마당",
    "새소식",
)

CATEGORY_KEYWORDS = {
    "학사 일정": ["학사", "일정", "시험", "방학", "개학", "수업"],
    "가정통신문": ["가정통신문", "학부모", "보호자"],
    "학생 생활": ["학생", "생활", "급식", "동아리", "봉사"],
    "진로·진학": ["진로", "진학", "대학", "입시"],
    "기타 공지": [],
}


def get_soup(url):
    """웹페이지를 가져옵니다. 접속 오류와 인코딩 문제를 처리합니다."""
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=12,
    )
    response.raise_for_status()

    if not response.encoding or response.encoding.lower() == "iso-8859-1":
        response.encoding = response.apparent_encoding or "utf-8"

    return BeautifulSoup(response.text, "html.parser")


def clean_text(value):
    return re.sub(r"\s+", " ", value or "").strip()


def valid_http_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except (ValueError, TypeError):
        return False


def find_board_url(home_url, manual_url=""):
    """홈페이지에서 공지사항 게시판 링크를 탐색합니다."""
    if manual_url.strip():
        if not valid_http_url(manual_url.strip()):
            raise ValueError("올바른 HTTP 또는 HTTPS 게시판 주소를 입력하세요.")
        return manual_url.strip(), None

    soup = get_soup(home_url)
    candidates = []

    for anchor in soup.find_all("a", href=True):
        title = clean_text(anchor.get_text(" ", strip=True))
        href = urljoin(home_url, anchor["href"])

        if not title or not valid_http_url(href):
            continue

        if any(word in title for word in BOARD_KEYWORDS):
            # 외부 사이트로 이동하는 무관한 링크는 제외합니다.
            if urlparse(href).netloc != urlparse(home_url).netloc:
                continue

            # 메뉴명이 명확한 링크를 우선합니다.
            score = 0
            if "공지사항" in title:
                score += 5
            if "공지" in title:
                score += 2
            if "가정통신문" in title:
                score += 1

            candidates.append((score, href, title))

    if not candidates:
        raise ValueError(
            "공지사항 메뉴를 자동으로 찾지 못했습니다. "
            "사이드바에 게시판 주소를 직접 입력해 주세요."
        )

    candidates.sort(key=lambda item: item[0], reverse=True)
    _, board_url, board_title = candidates[0]
    return board_url, board_title


def extract_date(text):
    """게시글 영역에서 날짜 형식을 찾아 표시합니다."""
    match = re.search(
        r"(20\d{2}[./-]\s?\d{1,2}[./-]\s?\d{1,2})",
        text,
    )
    if match:
        return re.sub(r"\s+", "", match.group(1)).replace("/", "-").replace(".", "-")
    return "날짜 미확인"


def parse_notices(board_url, limit=100):
    """게시판에서 게시글 후보를 수집합니다."""
    soup = get_soup(board_url)
    notices = []
    seen_urls = set()

    # 일반적인 표, 목록, 카드형 게시판을 모두 탐색합니다.
    for anchor in soup.find_all("a", href=True):
        title = clean_text(anchor.get_text(" ", strip=True))
        href = urljoin(board_url, anchor["href"])

        if len(title) < 3 or not valid_http_url(href):
            continue

        if urlparse(href).netloc != urlparse(board_url).netloc:
            continue

        lower_title = title.lower()

        # 메뉴, 로그인, 페이지 이동 링크 등을 제외합니다.
        excluded = [
            "로그인", "회원가입", "비밀번호", "다음 페이지",
            "이전 페이지", "맨 처음", "맨 끝", "검색",
            "더보기", "홈으로", "목록", "수정", "삭제",
        ]
        if any(word in title for word in excluded):
            continue

        # 게시글 상세 주소에 자주 쓰이는 패턴
        href_looks_like_post = bool(
            re.search(
                r"(ntt|article|board|view|bbs|idx|seq|no=|id=)",
                href,
                re.IGNORECASE,
            )
        )

        # 파일 다운로드나 스크립트 링크는 제외합니다.
        if (
            href.startswith(("javascript:", "mailto:", "tel:"))
            or re.search(r"\.(pdf|hwp|hwpx|xlsx?|docx?|zip)(\?|$)", href, re.I)
        ):
            continue

        if not href_looks_like_post and len(title) < 5:
            continue

        # 게시글 제목 주변의 행 또는 목록 항목에서 날짜를 찾습니다.
        container = anchor.find_parent(["tr", "li", "article"])
        if container is None:
            container = anchor.parent

        context_text = clean_text(
            container.get_text(" ", strip=True) if container else title
        )
        date = extract_date(context_text)

        # 첨부파일·중복 링크는 URL 기준으로 제거합니다.
        if href in seen_urls:
            continue
        seen_urls.add(href)

        notices.append(
            {
                "title": title,
                "url": href,
                "date": date,
                "context": context_text[:500],
            }
        )

        if len(notices) >= limit:
            break

    return notices


def classify_notice(title):
    for category, keywords in CATEGORY_KEYWORDS.items():
        if keywords and any(word in title for word in keywords):
            return category
    return "기타 공지"


# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.title("📣 오성 공지 알리미")
    st.caption("천안오성고등학교 학교 소식")

    st.markdown("---")
    st.subheader("게시판 설정")
    home_url = st.text_input(
        "학교 홈페이지 주소",
        value=HOME_URL,
        help="학교 홈페이지의 기본 주소입니다.",
    )
    manual_board_url = st.text_input(
        "공지사항 게시판 주소 (선택)",
        value="",
        placeholder="게시판 주소를 모르면 비워 두세요.",
        help="자동 탐색이 실패하면 공지사항 목록 페이지 주소를 입력하세요.",
    )

    st.markdown("---")
    st.caption("게시글 원문은 학교 홈페이지에서 확인하세요.")
    st.link_button("학교 홈페이지 열기", HOME_URL, use_container_width=True)


# -----------------------------
# 메인 화면
# -----------------------------
st.markdown(
    '<div class="main-title">📣 오성 공지 알리미</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">'
    '학교 공지를 한눈에 확인하고 필요한 소식을 빠르게 찾아보세요.'
    '</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([3, 1])
with left:
    st.subheader("학교 공지사항")
    st.caption("학교 홈페이지 게시글을 불러옵니다.")
with right:
    refresh = st.button(
        "🔄 공지 새로고침",
        use_container_width=True,
        type="primary",
    )

if refresh:
    st.cache_data.clear()

# 네트워크 요청 결과를 짧게 캐싱합니다.
@st.cache_data(ttl=180, show_spinner=False)
def load_notices(home, manual):
    board_url, board_title = find_board_url(home, manual)
    notices = parse_notices(board_url)
    return board_url, board_title, notices


try:
    with st.spinner("학교 홈페이지에서 공지를 확인하고 있습니다..."):
        board_url, board_title, notices = load_notices(
            home_url.strip(),
            manual_board_url.strip(),
        )

    st.success(
        f"게시판 연결 완료 · {board_title or '공지사항'}"
        f" · 게시글 {len(notices)}개"
    )
    st.caption(f"게시판 주소: {board_url}")

    if not notices:
        st.warning(
            "게시글을 찾지 못했습니다. 게시판 주소가 맞는지 확인하거나 "
            "홈페이지 구조에 맞게 수집 규칙을 조정해 주세요."
        )
        st.link_button("학교 게시판 직접 확인", board_url)
    else:
        for item in notices:
            item["category"] = classify_notice(item["title"])

        # 중요 공지 후보는 제목에 포함된 표현으로만 표시합니다.
        important_words = ["긴급", "필독", "중요", "제출 기한", "신청 마감"]
        important = [
            item for item in notices
            if any(word in item["title"] for word in important_words)
        ]

        m1, m2, m3 = st.columns(3)
        m1.metric("수집된 공지", f"{len(notices)}건")
        m2.metric("중요 공지 후보", f"{len(important)}건")
        m3.metric("분류 종류", f"{len(set(i['category'] for i in notices))}개")

        if important:
            with st.expander("🚨 중요 공지 후보", expanded=True):
                st.caption(
                    "제목의 특정 단어를 기준으로 찾은 결과이며, "
                    "학교가 공식 지정한 중요도는 아닙니다."
                )
                for item in important:
                    st.markdown(
                        f"- **[{item['title']}]({item['url']})** "
                        f"— {item['date']}"
                    )

        st.markdown("---")
        st.subheader("공지 검색")

        search_col, category_col = st.columns([2, 1])
        with search_col:
            keyword = st.text_input(
                "검색어",
                placeholder="예: 시험, 가정통신문, 방학",
            )
        with category_col:
            categories = ["전체"] + list(CATEGORY_KEYWORDS.keys())
            selected_category = st.selectbox("분류", categories)

        filtered = notices

        if keyword.strip():
            query = keyword.strip().lower()
            filtered = [
                item for item in filtered
                if query in item["title"].lower()
                or query in item["context"].lower()
            ]

        if selected_category != "전체":
            filtered = [
                item for item in filtered
                if item["category"] == selected_category
            ]

        st.caption(f"검색 결과: {len(filtered)}건")

        if not filtered:
            st.info("조건에 맞는 공지가 없습니다. 검색어를 바꿔 보세요.")
        else:
            for item in filtered:
                with st.container(border=True):
                    top1, top2 = st.columns([4, 1])
                    with top1:
                        st.markdown(f"### {item['title']}")
                        st.caption(
                            f"📅 {item['date']}　·　"
                            f"📂 {item['category']}"
                        )
                    with top2:
                        st.link_button(
                            "원문 보기 ↗",
                            item["url"],
                            use_container_width=True,
                        )

except requests.exceptions.Timeout:
    st.error("학교 홈페이지 응답 시간이 초과되었습니다. 잠시 후 다시 시도해 주세요.")
except requests.exceptions.HTTPError as exc:
    status = getattr(exc.response, "status_code", "알 수 없음")
    st.error(f"학교 홈페이지가 요청을 거부하거나 오류를 반환했습니다. HTTP {status}")
except requests.exceptions.RequestException:
    st.error(
        "학교 홈페이지에 연결할 수 없습니다. "
        "인터넷 연결과 홈페이지 주소를 확인해 주세요."
    )
except ValueError as exc:
    st.warning(str(exc))
except Exception as exc:
    # 예기치 못한 오류도 앱 전체 종료 대신 안내합니다.
    st.error(
        "공지사항을 처리하는 중 예상하지 못한 오류가 발생했습니다. "
        "게시판 주소와 홈페이지 구조를 확인해 주세요."
    )
    with st.expander("오류 상세 정보"):
        st.code(str(exc))

st.markdown("---")
st.caption(
    "본 서비스는 학교 공지를 편리하게 확인하기 위한 보조 도구입니다. "
    "제출 기한과 일정 등 중요한 내용은 반드시 학교의 공식 원문으로 확인하세요."
)

