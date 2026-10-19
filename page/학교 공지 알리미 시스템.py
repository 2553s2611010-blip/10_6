
import streamlit as st
from datetime import date, datetime
from urllib.parse import urlparse
import secrets

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="천안오성고 공지 알리미",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="expanded",
)

SCHOOL_NAME = "천안오성고등학교"
SCHOOL_URL = "http://ohseong.hs.kr"
CATEGORIES = [
    "학사 일정",
    "학교 행사",
    "시험",
    "가정통신문",
    "급식",
    "동아리",
    "기타",
]

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.8rem;
        border-radius: 18px;
        background: linear-gradient(120deg, #163b70, #2675b9);
        color: white;
        margin-bottom: 1.3rem;
    }
    .hero h1 { color: white; margin-bottom: .4rem; }
    .hero p { color: #e7f0ff; margin-bottom: 0; }
    .notice-box {
        padding: 1rem;
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 12px;
        margin-bottom: .6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 세션 데이터
# 주의: 앱 재시작 시 초기화됩니다.
# --------------------------------------------------
if "notices" not in st.session_state:
    st.session_state.notices = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False


def valid_url(value):
    """HTTP/HTTPS 링크만 허용합니다."""
    if not value:
        return True
    try:
        parsed = urlparse(value.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except (ValueError, AttributeError):
        return False


def get_admin_password():
    """Secrets에 설정된 관리자 비밀번호를 가져옵니다."""
    try:
        return str(st.secrets["ADMIN_PASSWORD"]).strip()
    except (KeyError, FileNotFoundError, TypeError):
        return ""


def format_date(value):
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return str(value)


def notice_sort_key(notice):
    return (
        bool(notice.get("important", False)),
        str(notice.get("date", "")),
        int(notice.get("id", 0)),
    )


def render_notice(notice, show_management=False):
    """공지 한 건을 표시합니다."""
    title = notice.get("title", "제목 없음")
    category = notice.get("category", "기타")
    content = notice.get("content", "")
    notice_date = notice.get("date", "")
    link = notice.get("url", "")

    with st.container(border=True):
        first, second = st.columns([5, 1])

        with first:
            labels = []
            if notice.get("important"):
                labels.append("📌 중요")
            labels.append(f"📂 {category}")
            st.caption(" · ".join(labels))
            st.subheader(title)
            st.caption(f"📅 {notice_date}")
        with second:
            if show_management:
                st.caption("관리자 화면")

        st.write(content)

        if link and valid_url(link):
            st.link_button(
                "공지 원문 열기 ↗",
                link,
                use_container_width=False,
            )

        notice_id = notice.get("id")
        if notice_id is not None:
            is_favorite = notice_id in st.session_state.favorites
            label = "★ 관심 공지 해제" if is_favorite else "☆ 관심 공지 저장"

            if st.button(label, key=f"fav_{notice_id}"):
                if is_favorite:
                    st.session_state.favorites.remove(notice_id)
                else:
                    st.session_state.favorites.append(notice_id)
                st.rerun()


# --------------------------------------------------
# 상단 헤더
# --------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
        <h1>📢 {SCHOOL_NAME} 공지 알리미</h1>
        <p>학교 소식을 빠르게 확인하고 중요한 안내를 놓치지 마세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 사이드바
# --------------------------------------------------
with st.sidebar:
    st.title("📚 메뉴")
    page = st.radio(
        "이동할 화면",
        ["공지 대시보드", "공지 전체 보기", "관심 공지", "관리자"],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### 🏫 학교 홈페이지")
    st.link_button(
        "공식 홈페이지 방문",
        SCHOOL_URL,
        use_container_width=True,
    )
    st.caption("공식 홈페이지에서 최신 원문을 확인하세요.")
    st.divider()
    st.caption(f"오늘 날짜: {date.today().isoformat()}")


# --------------------------------------------------
# 공지 목록 공통 처리
# --------------------------------------------------
notices = sorted(
    st.session_state.notices,
    key=notice_sort_key,
    reverse=True,
)

# --------------------------------------------------
# 1. 대시보드
# --------------------------------------------------
if page == "공지 대시보드":
    st.subheader("한눈에 보는 학교 소식")

    total = len(notices)
    important_count = sum(
        1 for item in notices if item.get("important")
    )
    favorite_count = len(st.session_state.favorites)

    a, b, c = st.columns(3)
    a.metric("등록된 공지", f"{total}건")
    b.metric("중요 공지", f"{important_count}건")
    c.metric("관심 공지", f"{favorite_count}건")

    st.divider()
    st.subheader("📌 중요 공지")

    important_notices = [
        item for item in notices if item.get("important")
    ]

    if important_notices:
        for item in important_notices[:3]:
            render_notice(item)
    else:
        st.info(
            "등록된 중요 공지가 없습니다. "
            "학교의 실제 공지는 공식 홈페이지에서 확인하세요."
        )

    st.divider()
    st.subheader("🕒 최근 등록된 공지")

    if notices:
        for item in notices[:5]:
            render_notice(item)
    else:
        st.info(
            "아직 등록된 공지가 없습니다. "
            "아래 버튼을 눌러 학교 공식 홈페이지를 확인하세요."
        )

    st.link_button("학교 공지 확인하기 ↗", SCHOOL_URL)

# --------------------------------------------------
# 2. 전체 공지 및 검색
# --------------------------------------------------
elif page == "공지 전체 보기":
    st.subheader("🔎 공지 검색")

    keyword = st.text_input(
        "검색어",
        placeholder="공지 제목이나 내용을 입력하세요.",
    )

    category_filter = st.selectbox(
        "분류",
        ["전체"] + CATEGORIES,
    )

    important_only = st.checkbox("중요 공지만 보기")

    filtered = []
    for item in notices:
        text = (
            str(item.get("title", ""))
            + " "
            + str(item.get("content", ""))
        ).casefold()

        if keyword.strip().casefold() not in text:
            continue
        if category_filter != "전체":
            if item.get("category") != category_filter:
                continue
        if important_only and not item.get("important"):
            continue

        filtered.append(item)

    st.caption(f"검색 결과: {len(filtered)}건")

    if filtered:
        for item in filtered:
            render_notice(item)
    else:
        st.info("조건에 맞는 공지가 없습니다.")
        st.link_button("학교 홈페이지에서 확인하기 ↗", SCHOOL_URL)

# --------------------------------------------------
# 3. 관심 공지
# --------------------------------------------------
elif page == "관심 공지":
    st.subheader("⭐ 내가 저장한 공지")

    favorites = [
        item for item in notices
        if item.get("id") in st.session_state.favorites
    ]

    if favorites:
        for item in favorites:
            render_notice(item)
    else:
        st.info(
            "아직 저장한 공지가 없습니다. "
            "공지 카드의 관심 공지 버튼을 눌러 저장하세요."
        )

# --------------------------------------------------
# 4. 관리자
# --------------------------------------------------
elif page == "관리자":
    st.subheader("🔐 공지 관리")

    admin_password = get_admin_password()

    if not admin_password:
        st.warning(
            "관리자 기능이 잠겨 있습니다. "
            "GitHub 저장소의 Streamlit Secrets에 "
            "ADMIN_PASSWORD를 설정하면 사용할 수 있습니다."
        )
        st.code('ADMIN_PASSWORD = "여기에_강력한_비밀번호"')
        st.info(
            "관리자 비밀번호를 설정하기 전까지는 "
            "공지 등록 및 삭제가 불가능합니다."
        )
    else:
        if not st.session_state.admin_authenticated:
            with st.form("admin_login"):
                password_input = st.text_input(
                    "관리자 비밀번호",
                    type="password",
                )
                login = st.form_submit_button(
                    "로그인",
                    use_container_width=True,
                )

            if login:
                if secrets.compare_digest(
                    password_input, admin_password
                ):
                    st.session_state.admin_authenticated = True
                    st.success("관리자 인증에 성공했습니다.")
                    st.rerun()
                else:
                    st.error("비밀번호가 올바르지 않습니다.")

        if st.session_state.admin_authenticated:
            if st.button("로그아웃"):
                st.session_state.admin_authenticated = False
                st.rerun()

            st.divider()
            st.markdown("### ✍️ 새 공지 등록")

            with st.form("notice_form", clear_on_submit=True):
                title = st.text_input(
                    "공지 제목",
                    max_chars=150,
                )
                category = st.selectbox(
                    "분류",
                    CATEGORIES,
                )
                notice_date = st.date_input(
                    "공지 날짜",
                    value=date.today(),
                )
                content = st.text_area(
                    "공지 내용",
                    height=180,
                    max_chars=10000,
                )
                url = st.text_input(
                    "공지 원문 URL (선택)",
                    placeholder="https://...",
                )
                important = st.checkbox("중요 공지로 표시")

                submitted = st.form_submit_button(
                    "공지 등록",
                    use_container_width=True,
                )

            if submitted:
                if not title.strip():
                    st.error("공지 제목을 입력하세요.")
                elif not content.strip():
                    st.error("공지 내용을 입력하세요.")
                elif not valid_url(url.strip()):
                    st.error(
                        "URL은 http:// 또는 https://로 시작해야 합니다."
                    )
                else:
                    next_id = (
                        max(
                            (
                                int(item.get("id", 0))
                                for item in st.session_state.notices
                            ),
                            default=0,
                        )
                        + 1
                    )

                    st.session_state.notices.append(
                        {
                            "id": next_id,
                            "title": title.strip(),
                            "category": category,
                            "date": format_date(notice_date),
                            "content": content.strip(),
                            "url": url.strip(),
                            "important": important,
                            "created_at": datetime.now().isoformat(
                                timespec="seconds"
                            ),
                        }
                    )
                    st.success("공지를 등록했습니다.")
                    st.rerun()

            st.divider()
            st.markdown("### 🗑️ 등록된 공지 관리")

            if not st.session_state.notices:
                st.info("삭제할 공지가 없습니다.")
            else:
                for item in sorted(
                    st.session_state.notices,
                    key=notice_sort_key,
                    reverse=True,
                ):
                    with st.container(border=True):
                        left, right = st.columns([5, 1])
                        with left:
                            st.write(f"**{item['title']}**")
                            st.caption(
                                f"{item['date']} · {item['category']}"
                            )
                        with right:
                            if st.button(
                                "삭제",
                                key=f"delete_{item['id']}",
                            ):
                                st.session_state.notices = [
                                    n for n in st.session_state.notices
                                    if n.get("id") != item.get("id")
                                ]
                                st.session_state.favorites = [
                                    fav for fav in st.session_state.favorites
                                    if fav != item.get("id")
                                ]
                                st.success("공지를 삭제했습니다.")
                                st.rerun()

st.divider()
st.caption(
    "천안오성고 공지 알리미 · 실제 공지 및 변경 사항은 "
    "학교 공식 홈페이지를 기준으로 확인하세요."
)
