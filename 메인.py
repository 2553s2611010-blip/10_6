
import streamlit as st
from urllib.parse import urlparse

st.set_page_config(
    page_title="새 학교 길잡이",
    page_icon="🎒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- 디자인 ----------
st.markdown("""
<style>
    .block-container {max-width: 1100px; padding-top: 2rem;}
    .hero {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(120deg, #e8f4ff, #edf8ef);
        margin-bottom: 1.5rem;
    }
    .hero h1 {color: #24476b; margin-bottom: .5rem;}
    .small-note {color: #64748b; font-size: .9rem;}
    div.stButton > button {border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# ---------- 안내 데이터 ----------
PAGES = {
    "학교생활": {
        "icon": "📚",
        "description": "학교생활에 필요한 기본 정보를 확인해요.",
        "sections": {
            "시간표 확인하기": [
                "학교 또는 담임 선생님에게 시간표를 확인해요.",
                "과목별 교과서와 준비물을 미리 챙겨요.",
                "교실이 바뀌는 수업이 있는지 확인해요.",
            ],
            "급식 이용하기": [
                "학교 급식표를 확인해요.",
                "급식실 위치와 이용 방법을 알아봐요.",
                "급식 관련 질문은 선생님께 문의해요.",
            ],
            "준비물 챙기기": [
                "필통, 공책 등 기본 학용품을 준비해요.",
                "과목별 준비물과 제출물을 확인해요.",
                "학교에서 안내한 준비 사항을 확인해요.",
            ],
        },
    },
    "학교 시설": {
        "icon": "🏫",
        "description": "학교의 주요 시설과 이용 방법을 알아봐요.",
        "sections": {
            "교무실": [
                "선생님을 찾아가거나 학교생활에 관해 질문할 때 이용해요.",
                "방문 전 해당 선생님의 위치를 확인해요.",
            ],
            "보건실": [
                "학교에서 몸이 아프거나 다쳤을 때 이용해요.",
                "이용 방법을 모르면 가까운 선생님께 도움을 요청해요.",
            ],
            "도서관": [
                "도서 대출과 반납 방법을 확인해요.",
                "도서관 운영 시간과 이용 규칙을 알아봐요.",
            ],
            "행정실": [
                "각종 학교 행정 관련 문의가 있을 때 이용해요.",
                "어떤 곳에 문의해야 할지 모르겠다면 담임 선생님께 물어봐요.",
            ],
        },
    },
    "친구 사귀기": {
        "icon": "🤝",
        "description": "새로운 친구들과 자연스럽게 가까워지는 방법이에요.",
        "sections": {
            "먼저 인사하기": [
                "옆자리 친구에게 밝게 인사해 봐요.",
                "이름을 소개하고 상대방의 이름도 물어봐요.",
            ],
            "대화 시작하기": [
                "수업이나 학교생활에 관해 가볍게 질문해 봐요.",
                "상대방의 이야기를 잘 듣고 공통 관심사를 찾아봐요.",
            ],
            "도움 요청하기": [
                "모르는 교실이나 규칙이 있다면 친구에게 물어봐요.",
                "어려운 일이 있으면 선생님에게 도움을 요청해도 괜찮아요.",
            ],
        },
    },
    "학교 규칙": {
        "icon": "📋",
        "description": "학교에서 지켜야 할 기본 규칙을 확인해요.",
        "sections": {
            "등교와 출결": [
                "등교 시간과 지각 처리 방법을 확인해요.",
                "결석이나 지각 시 필요한 절차를 알아봐요.",
            ],
            "교실 생활": [
                "수업 시간과 쉬는 시간의 규칙을 지켜요.",
                "교실과 공용 공간을 깨끗하게 사용해요.",
            ],
            "학교 공지 확인": [
                "학교 게시판이나 알림 서비스를 확인해요.",
                "중요한 제출 기한과 행사 일정을 기록해요.",
            ],
        },
    },
}


def valid_url(value):
    """HTTP 또는 HTTPS 주소만 허용."""
    try:
        parsed = urlparse(value.strip())
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
            and " " not in value.strip()
        )
    except (ValueError, AttributeError):
        return False


# ---------- 세션 상태 ----------
if "links" not in st.session_state:
    st.session_state.links = [
        {
            "name": "우리 학교 홈페이지",
            "url": "https://www.google.com",
            "category": "학교생활",
        },
        {
            "name": "학교 급식 정보 검색",
            "url": "https://www.google.com/search?q=학교+급식",
            "category": "학교생활",
        },
    ]

if "completed" not in st.session_state:
    st.session_state.completed = {}

if "page" not in st.session_state:
    st.session_state.page = "홈"

# ---------- 사이드바 ----------
with st.sidebar:
    st.title("🎒 새 학교 길잡이")
    st.caption("새로운 학교생활, 차근차근 시작해요!")
    st.divider()

    pages = ["홈", *PAGES.keys(), "안내 링크 관리", "적응 체크리스트"]
    selected = st.radio(
        "메뉴",
        pages,
        index=pages.index(st.session_state.page)
        if st.session_state.page in pages else 0,
    )
    st.session_state.page = selected

    st.divider()
    st.caption("학교별 실제 정보는 학교의 공식 안내를 확인하세요.")

# ---------- 홈 ----------
if selected == "홈":
    st.markdown("""
    <div class="hero">
        <h1>새 학교에 온 걸 환영해요! 🎉</h1>
        <p>처음이라 낯설어도 괜찮아요.</p>
        <p>학교생활에 필요한 정보를 하나씩 찾아봐요.</p>
    </div>
    """, unsafe_allow_html=True)

    search = st.text_input(
        "🔎 필요한 정보를 검색해 보세요",
        placeholder="예: 보건실, 급식, 친구",
    ).strip()

    if search:
        matches = []
        for category, data in PAGES.items():
            for section, tips in data["sections"].items():
                content = " ".join(tips)
                if search.lower() in (
                    category + section + data["description"] + content
                ).lower():
                    matches.append((category, section, tips))

        st.subheader("검색 결과")
        if matches:
            for category, section, tips in matches:
                with st.expander(f"{PAGES[category]['icon']} {category} · {section}"):
                    for tip in tips:
                        st.write(f"• {tip}")
        else:
            st.info("검색 결과가 없어요. 다른 단어로 검색해 보세요.")

    st.subheader("무엇이 궁금한가요?")

    categories = list(PAGES.items())
    for start in range(0, len(categories), 2):
        cols = st.columns(2)
        for col, (category, data) in zip(cols, categories[start:start + 2]):
            with col:
                with st.container(border=True):
                    st.subheader(f"{data['icon']} {category}")
                    st.write(data["description"])
                    if st.button(
                        "내용 확인하기",
                        key=f"home_{category}",
                        use_container_width=True,
                    ):
                        st.session_state.page = category
                        st.rerun()

    st.subheader("🔗 바로가기")
    for link in st.session_state.links:
        with st.container(border=True):
            st.write(f"**{link['name']}** · {link['category']}")
            st.link_button(
                "페이지 열기 ↗",
                link["url"],
                use_container_width=True,
            )

# ---------- 카테고리별 안내 ----------
elif selected in PAGES:
    data = PAGES[selected]
    st.title(f"{data['icon']} {selected} 안내")
    st.write(data["description"])
    st.caption("아래 항목을 눌러 자세한 안내를 확인해 보세요.")

    for section, tips in data["sections"].items():
        with st.expander(section, expanded=False):
            for tip in tips:
                st.write(f"• {tip}")

    matching_links = [
        link for link in st.session_state.links
        if link["category"] == selected
    ]

    st.subheader("관련 안내 페이지")
    if matching_links:
        for link in matching_links:
            st.link_button(
                f"{link['name']} ↗",
                link["url"],
                use_container_width=True,
            )
    else:
        st.info("아직 등록된 관련 링크가 없어요.")

# ---------- 안내 링크 관리 ----------
elif selected == "안내 링크 관리":
    st.title("🔗 안내 페이지 연결하기")
    st.write(
        "학교 홈페이지, 시간표, 급식표 등 필요한 페이지의 주소를 등록해 보세요."
    )

    with st.form("add_link_form", clear_on_submit=True):
        name = st.text_input("페이지 이름", placeholder="예: 학교 홈페이지")
        url = st.text_input("페이지 주소", placeholder="https://...")
        category = st.selectbox("연결할 메뉴", list(PAGES.keys()))
        submitted = st.form_submit_button("링크 추가")

        if submitted:
            clean_name = name.strip()
            clean_url = url.strip()

            if not clean_name:
                st.error("페이지 이름을 입력해 주세요.")
            elif not valid_url(clean_url):
                st.error("올바른 HTTP 또는 HTTPS 주소를 입력해 주세요.")
            elif any(
                item["url"] == clean_url
                for item in st.session_state.links
            ):
                st.warning("이미 등록된 주소예요.")
            else:
                st.session_state.links.append({
                    "name": clean_name,
                    "url": clean_url,
                    "category": category,
                })
                st.success("링크를 추가했어요!")
                st.rerun()

    st.divider()
    st.subheader("등록된 링크")

    if not st.session_state.links:
        st.info("등록된 링크가 없어요.")
    else:
        for i, link in enumerate(st.session_state.links):
            with st.container(border=True):
                st.write(f"**{link['name']}**")
                st.caption(f"분류: {link['category']}")
                st.code(link["url"], language=None)
                col1, col2 = st.columns(2)
                with col1:
                    st.link_button(
                        "페이지 열기 ↗",
                        link["url"],
                        use_container_width=True,
                        key=f"open_{i}",
                    )
                with col2:
                    if st.button(
                        "삭제",
                        key=f"delete_{i}",
                        use_container_width=True,
                    ):
                        st.session_state.links.pop(i)
                        st.rerun()

    st.caption(
        "안내: 링크는 현재 브라우저 세션에 저장됩니다. "
        "앱을 새로 시작하면 직접 추가한 링크가 유지되지 않을 수 있어요."
    )

# ---------- 적응 체크리스트 ----------
elif selected == "적응 체크리스트":
    st.title("✅ 나의 학교 적응 체크리스트")
    st.write("확인한 항목에 체크해 보세요.")

    tasks = [
        ("학교 건물과 교실 위치 알아보기", "장소"),
        ("시간표와 교과서 확인하기", "수업"),
        ("급식실 위치와 이용 방법 알아보기", "생활"),
        ("담임 선생님과 주요 연락 방법 확인하기", "도움"),
        ("학교 규칙과 출결 방법 확인하기", "규칙"),
        ("반 친구에게 먼저 인사해 보기", "친구"),
        ("학교 공지 확인하는 방법 알아보기", "공지"),
    ]

    completed_count = sum(
        bool(st.session_state.completed.get(task, False))
        for task, _ in tasks
    )
    st.progress(completed_count / len(tasks))
    st.write(f"완료한 항목: **{completed_count}/{len(tasks)}**")

    for task, category in tasks:
        key = f"task_{task}"
        checked = st.checkbox(
            task,
            value=st.session_state.completed.get(task, False),
            key=key,
        )
        st.session_state.completed[task] = checked

    if completed_count == len(tasks):
        st.success("모든 항목을 확인했어요! 새로운 학교생활을 응원해요 🎉")
    else:
        st.info("모든 항목을 한 번에 끝내지 않아도 괜찮아요.")

# ---------- 공통 하단 ----------
st.divider()
st.caption(
    "새 학교 길잡이 | 학교생활 적응을 돕기 위한 안내 앱입니다. "
    "실제 학교 정보는 학교의 공식 공지를 기준으로 확인하세요."
)

