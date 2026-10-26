
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests
import streamlit as st


# ==========================================
# 1. 기본 설정
# ==========================================
st.set_page_config(
    page_title="천안오성고 공지 알리미",
    page_icon="📣",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_HOME = "https://ohsung.caehs.kr"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    )
}

BOARD_WORDS = [
    "공지사항",
    "공지",
    "가정통신문",
    "학교소식",
    "알림마당",
    "새소식",
]

CATEGORY_WORDS = {
    "학사 일정": [
        "학사", "일정", "시험", "방학", "개학", "수업", "시간표"
    ],
    "가정통신문": [
        "가정통신문", "학부모", "보호자"
    ],
    "학생 생활": [
        "학생", "생활", "급식", "동아리", "봉사"
    ],
    "진로·진학": [
        "진로", "진학", "대학", "입시"
    ],
    "기타 공지": [],
}

IMPORTANT_WORDS = [
    "긴급", "필독", "중요", "제출 기한", "신청 마감"
]


# ==========================================
# 2. 화면 디자인
# ==========================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fb;
    }

    .hero {
        background: linear-gradient(120deg, #173b70, #3478bd);
        color: white;
        padding: 28px;
        border-radius: 18px;
        margin-bottom: 20px;
    }

    .hero h1 {
        font-size: 30px;
        margin: 0 0 10px 0;
    }

    .hero p {
        margin: 0;
        opacity: 0.92;
    }

    .small-note {
        color: #65748b;
        font-size: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>📣 오성 공지 알리미</h1>
        <p>천안오성고등학교의 소식을 한곳에서 확인하세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# 3. HTML 링크 추출기
#    외부 라이브러리 bs4 불필요
# ==========================================
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.current_href = None
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self.current_href = dict(attrs).get("href")
            self.current_text = []

    def handle_data(self, data):
        if self.current_href is not None:
            self.current_text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self.current_href is not None:
            title = clean_text(" ".join(self.current_text))

            if title and self.current_href:
                self.links.append({
                    "title": title,
                    "href": self.current_href,
                })

            self.current_href = None
            self.current_text = []


def clean_text(text):
    """불필요한 공백과 줄바꿈을 정리합니다."""
    return re.sub(r"\s+", " ", str(text or "")).strip()


def is_web_url(url):
    """HTTP/HTTPS 주소인지 확인합니다."""
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
        )
    except (ValueError, TypeError):
        return False


def fetch_html(url):
    """웹페이지를 요청하고 HTML을 반환합니다."""
    if not is_web_url(url):
        raise ValueError("HTTP 또는 HTTPS 주소를 입력해 주세요.")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()

    if not response.encoding or response.encoding.lower() == "iso-8859-1":
        response.encoding = response.apparent_encoding or "utf-8"

    return response.text


def extract_links(html, base_url):
    """HTML에서 유효한 링크를 추출합니다."""
    parser = LinkParser()
    parser.feed(html)

    results = []
    base_host = urlparse(base_url).netloc

    for link in parser.links:
        title = clean_text(link["title"])
        href = urljoin(base_url, link["href"])

        if not title or not is_web_url(href):
            continue

        # 외부 사이트로 이동하는 링크 제외
        if urlparse(href).netloc != base_host:
            continue

        if href.lower().startswith(("javascript:", "mailto:", "tel:")):
            continue

        results.append({
            "title": title,
            "url": href,
        })

    return results


def find_board(home_url, manual_url=""):
    """사용자가 입력한 게시판 주소 또는 홈페이지 메뉴를 확인합니다."""
    if manual_url.strip():
        board_url = manual_url.strip()

        if not is_web_url(board_url):
            raise ValueError(
                "게시판 주소는 https:// 또는 http://로 시작해야 합니다."
            )

        return board_url, "직접 입력한 게시판"

    html = fetch_html(home_url)
    links = extract_links(html, home_url)

    candidates = []

    for link in links:
        title = link["title"]

        if any(word in title for word in BOARD_WORDS):
            score = 0

            if "공지사항" in title:
                score += 10
            elif title == "공지":
                score += 7

            if "가정통신문" in title:
                score += 2

            candidates.append(
                (score, link["url"], title)
            )

    if not candidates:
        raise ValueError(
            "홈페이지에서 공지사항 메뉴를 자동으로 찾지 못했습니다. "
            "사이드바에 실제 공지사항 목록 주소를 입력해 주세요."
        )

    candidates.sort(key=lambda item: item[0], reverse=True)

    _, url, title = candidates[0]
    return url, title


def extract_date(text):
    """텍스트에서 날짜를 찾습니다."""
    match = re.search(
        r"20\d{2}\s*[./-]\s*\d{1,2}\s*[./-]\s*\d{1,2}",
        text,
    )

    if not match:
        return "날짜 미확인"

    value = re.sub(r"\s+", "", match.group(0))
    return value.replace("/", "-").replace(".", "-")


def parse_notices(board_url, limit=100):
    """게시판의 링크를 분석해 공지 후보를 만듭니다."""
    html = fetch_html(board_url)
    links = extract_links(html, board_url)

    notices = []
    seen = set()

    excluded_words = [
        "로그인", "회원가입", "비밀번호", "검색",
        "다음 페이지", "이전 페이지", "더보기",
        "홈으로", "목록", "수정", "삭제",
    ]

    for link in links:
        title = clean_text(link["title"])
        url = link["url"]

        if len(title) < 3:
            continue

        if any(word in title for word in excluded_words):
            continue

        # 첨부파일 주소는 공지 목록에서 제외
        if re.search(
            r"\.(pdf|hwp|hwpx|xlsx?|docx?|zip)(\?|$)",
            url,
            re.IGNORECASE,
        ):
            continue

        if url in seen:
            continue

        seen.add(url)

        # 링크만으로 날짜가 확인되지 않으면 별도 표시
        date = "날짜 미확인"

        notices.append({
            "title": title,
            "url": url,
            "date": date,
            "category": classify_notice(title),
        })

        if len(notices) >= limit:
            break

    return notices


def classify_notice(title):
    """제목의 키워드로 공지를 분류합니다."""
    for category, keywords in CATEGORY_WORDS.items():
        if keywords and any(word in title for word in keywords):
            return category

    return "기타 공지"


def is_important(title):
    """중요 키워드가 있는 제목인지 확인합니다."""
    return any(word in title for word in IMPORTANT_WORDS)


# ==========================================
# 4. 사이드바 설정
# ==========================================
with st.sidebar:
    st.title("⚙️ 설정")

    home_url = st.text_input(
        "학교 홈페이지 주소",
        value=DEFAULT_HOME,
    )

    manual_board_url = st.text_input(
        "공지사항 게시판 주소",
        value="",
        placeholder="모르면 비워 두세요.",
        help=(
            "자동 탐색이 실패한다면 학교 홈페이지의 "
            "공지사항 목록 페이지 주소를 입력하세요."
        ),
    )

    st.caption(
        "학교 홈페이지가 일반적인 HTML 링크를 제공하지 않으면 "
        "자동 탐색이 실패할 수 있습니다."
    )

    st.divider()

    st.markdown("**이용 안내**")
    st.write("• 공지 검색 및 분류")
    st.write("• 중요 키워드 확인")
    st.write("• 학교 원문 바로가기")

    if is_web_url(home_url.strip()):
        st.link_button(
            "학교 홈페이지 열기 ↗",
            home_url.strip(),
            use_container_width=True,
        )


# ==========================================
# 5. 공지사항 가져오기
# ==========================================
col_title, col_button = st.columns([3, 1])

with col_title:
    st.subheader("🏫 학교 공지사항")
    st.caption("학교 홈페이지에서 게시글 정보를 가져옵니다.")

with col_button:
    refresh = st.button(
        "🔄 새로고침",
        use_container_width=True,
        type="primary",
    )

if refresh:
    st.cache_data.clear()


@st.cache_data(ttl=180, show_spinner=False)
def load_notices(home, manual):
    board_url, board_title = find_board(home, manual)
    notices = parse_notices(board_url)
    return board_url, board_title, notices


try:
    with st.spinner("공지사항을 불러오는 중입니다..."):
        board_url, board_title, notices = load_notices(
            home_url.strip(),
            manual_board_url.strip(),
        )

    st.success(f"게시판 연결 완료: {board_title}")
    st.caption(f"게시판 주소: {board_url}")

    if not notices:
        st.warning(
            "게시글을 찾지 못했습니다. 게시판 주소가 맞는지 확인해 주세요."
        )
        st.link_button("게시판 직접 열기 ↗", board_url)

    else:
        important_notices = [
            item for item in notices
            if is_important(item["title"])
        ]

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric("수집된 링크", f"{len(notices)}건")
        metric2.metric("중요 키워드", f"{len(important_notices)}건")
        metric3.metric(
            "분류 종류",
            f"{len(set(item['category'] for item in notices))}개",
        )

        if important_notices:
            with st.expander(
                "🚨 중요 공지 후보",
                expanded=True,
            ):
                st.caption(
                    "제목에 중요 키워드가 포함된 게시물입니다. "
                    "학교의 공식 중요 공지 지정과는 다를 수 있습니다."
                )

                for item in important_notices:
                    st.markdown(
                        f"- [{item['title']}]({item['url']})"
                    )

        st.divider()
        st.subheader("🔎 공지 검색")

        search_col, category_col = st.columns([2, 1])

        with search_col:
            keyword = st.text_input(
                "검색어",
                placeholder="예: 시험, 방학, 가정통신문",
            )

        with category_col:
            selected_category = st.selectbox(
                "공지 분류",
                [
                    "전체",
                    "학사 일정",
                    "가정통신문",
                    "학생 생활",
                    "진로·진학",
                    "기타 공지",
                ],
            )

        filtered = notices

        if keyword.strip():
            search_term = keyword.strip().casefold()

            filtered = [
                item for item in filtered
                if search_term in item["title"].casefold()
            ]

        if selected_category != "전체":
            filtered = [
                item for item in filtered
                if item["category"] == selected_category
            ]

        st.caption(f"검색 결과 {len(filtered)}건")

        if not filtered:
            st.info("검색 결과가 없습니다. 검색어를 바꿔 보세요.")

        for item in filtered:
            with st.container(border=True):
                left, right = st.columns([4, 1])

                with left:
                    if is_important(item["title"]):
                        st.markdown(f"**🚨 {item['title']}**")
                    else:
                        st.markdown(f"**{item['title']}**")

                    st.caption(
                        f"분류: {item['category']} · "
                        f"날짜: {item['date']}"
                    )

                with right:
                    st.link_button(
                        "원문 보기 ↗",
                        item["url"],
                        use_container_width=True,
                    )

except requests.exceptions.Timeout:
    st.error(
        "학교 홈페이지 응답 시간이 초과되었습니다. "
        "잠시 후 다시 시도해 주세요."
    )

except requests.exceptions.HTTPError as exc:
    status_code = (
        exc.response.status_code
        if exc.response is not None
        else "확인 불가"
    )
    st.error(
        f"학교 홈페이지에서 HTTP {status_code} 오류가 발생했습니다. "
        "주소와 접속 가능 여부를 확인해 주세요."
    )

except requests.exceptions.RequestException:
    st.error(
        "학교 홈페이지에 연결하지 못했습니다. "
        "인터넷 연결과 홈페이지 주소를 확인해 주세요."
    )

except ValueError as exc:
    st.warning(str(exc))

except Exception:
    st.error(
        "공지사항 처리 중 예상하지 못한 오류가 발생했습니다. "
        "게시판 주소를 확인한 후 다시 시도해 주세요."
    )

st.divider()

st.markdown(
    """
    <p class="small-note">
    본 앱은 학교 공지 확인을 돕는 보조 서비스입니다.
    중요한 일정과 제출 기한은 반드시 학교 공식 홈페이지의 원문으로 확인하세요.
    </p>
    """,
    unsafe_allow_html=True,
)
