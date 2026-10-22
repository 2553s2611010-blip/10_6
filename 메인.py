
import streamlit as st

st.set_page_config(
    page_title="천안오성고등학교 | 전학생 안내",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 색상 및 디자인
# -----------------------------
NAVY = "#101D35"
BLUE = "#416C9B"
LIGHT_BLUE = "#EAF1FA"
TEXT = "#17263D"
MUTED = "#66758A"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Noto Sans KR', sans-serif;
    }}

    .stApp {{
        background: #F5F7FB;
        color: {TEXT};
    }}

    [data-testid="stHeader"] {{
        background: rgba(245,247,251,0.95);
    }}

    [data-testid="stSidebar"] {{
        background: {NAVY};
    }}

    [data-testid="stSidebar"] * {{
        color: #F1F5FC;
    }}

    .hero {{
        background: linear-gradient(120deg, #101D35 0%, #203F66 65%, #416C9B 100%);
        padding: 42px 38px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
    }}

    .hero-label {{
        color: #C2D8F5;
        font-size: 12px;
        letter-spacing: 3px;
        font-weight: 700;
    }}

    .hero h1 {{
        color: white;
        font-size: clamp(28px, 4vw, 43px);
        line-height: 1.35;
        margin: 16px 0 10px 0;
        font-weight: 800;
    }}

    .hero p {{
        color: #E0E9F5;
        font-size: 15px;
        line-height: 1.8;
        margin-bottom: 0;
    }}

    .section-title {{
        color: {NAVY};
        font-size: 23px;
        font-weight: 800;
        margin: 28px 0 6px 0;
    }}

    .section-desc {{
        color: {MUTED};
        font-size: 14px;
        margin-bottom: 18px;
    }}

    .info-card {{
        background: white;
        border: 1px solid #E3E9F2;
        border-radius: 15px;
        padding: 22px;
        min-height: 150px;
        margin-bottom: 12px;
    }}

    .card-number {{
        font-size: 12px;
        color: {BLUE};
        letter-spacing: 1.5px;
        font-weight: 800;
    }}

    .card-title {{
        color: {NAVY};
        font-size: 18px;
        font-weight: 700;
        margin: 12px 0 8px 0;
    }}

    .card-desc {{
        color: {MUTED};
        font-size: 13px;
        line-height: 1.8;
    }}

    .notice {{
        background: {LIGHT_BLUE};
        border-left: 4px solid {BLUE};
        padding: 16px 18px;
        border-radius: 8px;
        color: {TEXT};
        line-height: 1.8;
        margin: 14px 0;
    }}

    .footer {{
        text-align: center;
        color: #8793A5;
        font-size: 12px;
        padding: 30px 0 10px 0;
    }}

    div.stButton > button {{
        border-radius: 10px;
        min-height: 44px;
        font-weight: 600;
        border: 1px solid #DCE5F0;
    }}

    div.stButton > button[kind="primary"] {{
        background: {NAVY};
        border-color: {NAVY};
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 안내 페이지 데이터
# -----------------------------
PAGES = {
    "학교 소개": {
        "icon": "🏫",
        "desc": "학교와 새로운 환경 알아보기",
        "intro": "새로운 학교생활의 첫걸음",
        "items": [
            ("학교 기본 정보", "학교의 공식 홈페이지와 공지사항에서 학교 정보를 확인해 보세요."),
            ("학교 시설", "교실, 교무실, 보건실, 도서관 등 주요 시설의 위치를 확인해 보세요."),
            ("학교 규칙", "등교 시간, 복장, 출결 등 학교생활에 필요한 규칙을 확인해 보세요."),
        ],
    },
    "학교생활": {
        "icon": "🧭",
        "desc": "교실과 학교 시설 이용하기",
        "intro": "학교 안에서 길을 잃지 않도록",
        "items": [
            ("교실 찾기", "배정받은 학년과 반을 확인하고 교실 위치를 담임 선생님께 문의하세요."),
            ("주요 시설", "교무실, 보건실, 도서관 등 자주 이용할 시설의 위치를 알아두세요."),
            ("도움 요청하기", "학교생활이 낯설다면 담임 선생님이나 담당 선생님께 도움을 요청하세요."),
        ],
    },
    "일과 및 학습": {
        "icon": "📅",
        "desc": "하루 일과와 학습 준비",
        "intro": "하루의 흐름을 미리 준비하기",
        "items": [
            ("하루 일과", "정확한 등교 시간과 수업 시간은 학교에서 안내하는 최신 시간표를 확인하세요."),
            ("수업 준비", "과목별 교과서, 필기구, 학습 자료를 미리 준비하세요."),
            ("과제와 평가", "수행평가 일정과 과제 제출 방법은 교과 담당 선생님께 확인하세요."),
        ],
    },
    "친구 관계와 적응": {
        "icon": "🤝",
        "desc": "새로운 친구들과 친해지기",
        "intro": "천천히 익숙해져도 괜찮아요",
        "items": [
            ("먼저 인사하기", "가벼운 인사와 자기소개로 자연스럽게 대화를 시작해 보세요."),
            ("함께 활동하기", "모둠 활동이나 동아리에서 친구들과 대화할 기회를 만들어 보세요."),
            ("어려움 이야기하기", "적응이 어렵거나 고민이 있다면 믿을 수 있는 선생님에게 이야기하세요."),
        ],
    },
    "자주 묻는 질문": {
        "icon": "💬",
        "desc": "전학생이 궁금해하는 내용",
        "intro": "궁금한 점을 빠르게 해결하기",
        "items": [
            ("반 배정은 어디서 확인하나요?", "담임 선생님 또는 학교에서 안내하는 공식 절차를 통해 확인하세요."),
            ("시간표는 어디서 확인하나요?", "학교에서 배부하는 시간표나 공식 학사 안내를 확인하세요."),
            ("준비물을 모르겠어요.", "해당 과목 선생님이나 담임 선생님께 문의하면 정확하게 확인할 수 있어요."),
            ("학교생활에 적응하기 어려워요.", "담임 선생님, 상담 담당 선생님 등 믿을 수 있는 어른에게 도움을 요청하세요."),
            ("급식 메뉴는 어디서 확인하나요?", "학교 공식 홈페이지의 급식 안내를 확인하세요."),
        ],
    },
}

if "page" not in st.session_state:
    st.session_state.page = "홈"

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.markdown("## 🏫 OSEONG")
    st.caption("CHEONAN OSEONG HIGH SCHOOL")
    st.markdown("---")
    st.markdown("### GUIDE MENU")

    if st.button("⌂  메인 페이지", use_container_width=True):
        st.session_state.page = "홈"
        st.rerun()

    for name, data in PAGES.items():
        if st.button(
            f"{data['icon']}  {name}",
            key=f"nav_{name}",
            use_container_width=True,
        ):
            st.session_state.page = name
            st.rerun()

    st.markdown("---")
    st.caption("새로운 시작을 응원합니다.")
    st.caption("Transfer Student Guide")

# -----------------------------
# 메인 페이지
# -----------------------------
def render_home():
    st.markdown(
        """
        <div class="hero">
            <div class="hero-label">CHEONAN OSEONG HIGH SCHOOL</div>
            <h1>새로운 학교생활,<br>여기서 시작하세요.</h1>
            <p>
                천안오성고등학교에 온 여러분을 환영합니다.<br>
                학교생활에 필요한 정보를 한곳에서 확인해 보세요.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">YOUR SCHOOL GUIDE</div>'
        '<div class="section-desc">필요한 안내를 선택해 보세요.</div>',
        unsafe_allow_html=True,
    )

    # 검색
    keyword = st.text_input(
        "🔎 안내 검색",
        placeholder="예: 시간표, 교실, 친구, 급식",
        key="home_search",
    )

    if keyword.strip():
        matches = []
        for name, data in PAGES.items():
            searchable = (
                name + " " + data["desc"] + " " + data["intro"] + " "
                + " ".join(title + " " + desc for title, desc in data["items"])
            )
            if keyword.strip().lower() in searchable.lower():
                matches.append(name)

        st.markdown("#### 검색 결과")
        if matches:
            for name in matches:
                if st.button(
                    f"{PAGES[name]['icon']}  {name} — {PAGES[name]['desc']}",
                    key=f"search_{name}",
                    use_container_width=True,
                ):
                    st.session_state.page = name
                    st.rerun()
        else:
            st.info("검색 결과가 없습니다. 다른 단어로 검색해 보세요.")

    st.markdown("")

    names = list(PAGES.keys())
    for start in range(0, len(names), 2):
        cols = st.columns(2)
        for offset, name in enumerate(names[start:start + 2]):
            data = PAGES[name]
            with cols[offset]:
                st.markdown(
                    f"""
                    <div class="info-card">
                        <div class="card-number">GUIDE / {start + offset + 1:02d}</div>
                        <div class="card-title">{data['icon']} &nbsp; {name}</div>
                        <div class="card-desc">{data['desc']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(
                    f"{name} 자세히 보기  →",
                    key=f"home_{name}",
                    use_container_width=True,
                    type="primary",
                ):
                    st.session_state.page = name
                    st.rerun()

    st.markdown(
        """
        <div class="notice">
            <b>처음 학교에 왔다면?</b><br>
            학교 소개를 먼저 확인한 뒤 학교생활, 일과 및 학습 안내를
            차례대로 살펴보세요. 정확한 학교 정보는 공식 안내를 기준으로 확인하세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# 세부 안내 페이지
# -----------------------------
def render_page(name):
    data = PAGES[name]

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-label">STUDENT INFORMATION GUIDE</div>
            <h1>{data['icon']} &nbsp; {name}</h1>
            <p>{data['intro']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(f"홈 / {name}")
    st.markdown("")

    for index, (title, desc) in enumerate(data["items"], start=1):
        with st.container(border=True):
            st.markdown(f"### {index:02d}  {title}")
            st.write(desc)

    st.markdown(
        """
        <div class="notice">
            안내 내용은 학교생활을 위한 기본 참고 정보입니다.
            실제 시간표, 시설 위치, 학사 일정 및 학교 규정은
            학교의 공식 공지나 담당 선생님을 통해 확인하세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 다른 안내 페이지")
    others = [page for page in PAGES if page != name]
    cols = st.columns(2)

    for index, other in enumerate(others):
        with cols[index % 2]:
            if st.button(
                f"{PAGES[other]['icon']}  {other}  →",
                key=f"other_{name}_{other}",
                use_container_width=True,
            ):
                st.session_state.page = other
                st.rerun()

    if st.button("← 메인 페이지로 돌아가기", type="primary"):
        st.session_state.page = "홈"
        st.rerun()

# -----------------------------
# 화면 실행
# -----------------------------
try:
    if st.session_state.page == "홈":
        render_home()
    elif st.session_state.page in PAGES:
        render_page(st.session_state.page)
    else:
        st.session_state.page = "홈"
        st.rerun()

except Exception:
    st.error("화면을 표시하는 중 문제가 발생했습니다.")
    st.info("페이지를 새로고침하거나 메인 페이지로 돌아가 다시 시도해 주세요.")

st.markdown(
    """
    <div class="footer">
        CHEONAN OSEONG HIGH SCHOOL · STUDENT GUIDE<br>
        본 페이지는 학교생활 안내를 위한 예시 웹앱입니다.
    </div>
    """,
    unsafe_allow_html=True,
)

