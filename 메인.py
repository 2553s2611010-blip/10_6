
import streamlit as st

st.set_page_config(
    page_title="천안오성고등학교 길잡이",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# 디자인 CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #F4F7FB;
    --surface: #FFFFFF;
    --blue: #E5EDF8;
    --blue-strong: #6687B4;
    --mint: #DDECE8;
    --text: #293B52;
    --muted: #718096;
    --border: #E1E7EF;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
}

.block-container {
    max-width: 1120px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--text);
    letter-spacing: -0.035em;
}

h1 {
    font-weight: 800;
}

h2, h3 {
    font-weight: 650;
}

[data-testid="stSidebar"] {
    background: #EDF2F8;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] h1 {
    font-size: 1.35rem;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 10px;
}

.hero {
    background: linear-gradient(
        120deg,
        #E5EDF8 0%,
        #EAF1F7 65%,
        #DDECE8 100%
    );
    border: 1px solid #DEE7F0;
    border-radius: 22px;
    padding: 34px;
    margin-bottom: 28px;
}

.hero h1 {
    color: #293F5B;
    font-size: 2.1rem;
    margin-bottom: 12px;
}

.hero p {
    color: #586D84;
    font-size: 1rem;
    line-height: 1.8;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border-color: var(--border) !important;
    border-radius: 17px;
}

div.stButton > button,
div.stLinkButton > a {
    border-radius: 11px;
    font-weight: 600;
    transition: all 0.2s ease;
}

div.stButton > button {
    border: 1px solid #D7E1EE;
    background: #F1F5FA;
    color: #344D6B;
}

div.stButton > button:hover {
    border-color: #9DB4D2;
    background: #E5EDF8;
    color: #263D59;
}

div.stLinkButton > a {
    border: 1px solid #D7E1EE;
    background: #FFFFFF;
    color: #405B7C;
}

div.stLinkButton > a:hover {
    background: #EAF1F8;
    border-color: #A8BCD4;
}

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

[data-testid="stTextInput"] input {
    border-radius: 11px;
    border-color: #D8E1EB;
    background: #FFFFFF;
}

[data-testid="stProgressBar"] > div > div {
    background: #7798B8;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 15px;
}

hr {
    border-color: #E1E7EF;
}

.small-note {
    color: var(--muted);
    font-size: 0.9rem;
}

@media (max-width: 640px) {
    .block-container {
        padding: 1.2rem 1rem 2rem;
    }

    .hero {
        padding: 23px;
        border-radius: 17px;
    }

    .hero h1 {
        font-size: 1.65rem;
    }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "checked_items" not in st.session_state:
    st.session_state.checked_items = []

if "custom_links" not in st.session_state:
    st.session_state.custom_links = []


# -----------------------------
# 사이드바 메뉴
# -----------------------------
with st.sidebar:
    st.markdown("# 🎓 오성고 길잡이")
    st.caption("천안오성고등학교 학교생활 안내")

    page = st.radio(
        "메뉴",
        [
            "🏠 홈",
            "📚 학교생활",
            "🏫 학교 시설",
            "🤝 친구 사귀기",
            "📌 학교생활 팁",
            "🔗 유용한 링크",
            "✅ 준비물 체크리스트"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.caption("처음 시작하는 학교생활,\n차근차근 알아봐요.")


# -----------------------------
# 공통 카드 함수
# -----------------------------
def info_card(title, description, icon="📘"):
    with st.container(border=True):
        st.markdown(f"### {icon} {title}")
        st.write(description)


def link_card(title, description, url):
    with st.container(border=True):
        st.markdown(f"### {title}")
        st.write(description)
        st.link_button("바로가기 ↗", url, use_container_width=True)


# -----------------------------
# 홈
# -----------------------------
if page == "🏠 홈":
    st.markdown("""
    <div class="hero">
        <p>CHEONAN OHSEONG HIGH SCHOOL</p>
        <h1>새로운 학교생활의 시작</h1>
        <p>
            천안오성고등학교에 처음 온 학생들을 위한 안내 페이지예요.<br>
            학교생활에 필요한 정보와 유용한 사이트를 한곳에서 확인해 보세요.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("무엇이 궁금한가요?")
    st.caption("필요한 메뉴를 선택해 학교생활 정보를 확인해 보세요.")

    col1, col2 = st.columns(2)

    with col1:
        info_card(
            "학교생활",
            "시간표와 급식 정보, 학교생활에 유용한 내용을 확인해요.",
            "📚"
        )
        info_card(
            "친구 사귀기",
            "새로운 친구에게 자연스럽게 다가가는 방법을 알아봐요.",
            "🤝"
        )

    with col2:
        info_card(
            "학교 시설",
            "교실과 주요 시설을 찾을 때 참고할 내용을 확인해요.",
            "🏫"
        )
        info_card(
            "준비물 체크리스트",
            "학교에 가져갈 물건을 체크하며 준비해요.",
            "✅"
        )

    st.divider()
    st.subheader("학교 기본 정보")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**학교명**")
        st.write("천안오성고등학교")

        st.markdown("**주소**")
        st.write("충청남도 천안시 서북구 과수원길 27")

    with col2:
        st.markdown("**공식 홈페이지**")
        st.link_button(
            "학교 홈페이지 방문 ↗",
            "http://ohsung.caehs.kr"
        )

        st.markdown("**안내**")
        st.write("학교의 최신 공지와 일정은 공식 홈페이지에서 확인하세요.")


# -----------------------------
# 학교생활
# -----------------------------
elif page == "📚 학교생활":
    st.title("📚 학교생활")
    st.write("학교생활에 필요한 정보를 빠르게 확인해 보세요.")

    st.info(
        "시간표와 급식 정보는 외부 사이트로 연결돼요. "
        "정보가 변경될 수 있으니 학교 공지도 함께 확인하세요."
    )

    col1, col2 = st.columns(2)

    with col1:
        link_card(
            "🗓️ 시간표 확인",
            "수업 시간표를 확인할 수 있는 외부 사이트예요.",
            "https://www.classroutine.net/schools/N10/8140246"
        )

    with col2:
        link_card(
            "🍱 급식 정보 확인",
            "급식 메뉴를 확인할 수 있는 외부 사이트예요.",
            "https://school.weingchicken.com/schools/8584"
        )

    st.subheader("학교생활 기본 팁")

    info_card(
        "시간표 미리 확인하기",
        "다음 날 수업과 과목별 준비물을 전날 확인하면 편리해요.",
        "🗓️"
    )

    info_card(
        "학교 공지 확인하기",
        "수행평가, 행사, 제출 기한 등은 학교 공지를 통해 확인해요.",
        "📢"
    )

    info_card(
        "모르는 내용 질문하기",
        "교과 선생님이나 담임 선생님에게 질문하면 정확한 정보를 얻을 수 있어요.",
        "💬"
    )


# -----------------------------
# 학교 시설
# -----------------------------
elif page == "🏫 학교 시설":
    st.title("🏫 학교 시설 안내")
    st.write("학교 시설의 위치를 알아두면 처음 학교에 왔을 때 도움이 돼요.")

    info_card(
        "교실",
        "교실 번호와 층수를 확인하고 이동 경로를 미리 알아두세요.",
        "🚪"
    )

    info_card(
        "교무실",
        "선생님께 질문하거나 학교생활에 관한 도움을 받을 때 방문할 수 있어요.",
        "👩‍🏫"
    )

    info_card(
        "도서관",
        "독서와 과제에 필요한 자료를 찾아볼 수 있는 공간이에요.",
        "📖"
    )

    info_card(
        "보건실",
        "학교에서 몸이 아프거나 다쳤을 때 선생님에게 알리고 도움을 요청하세요.",
        "🩺"
    )

    st.warning(
        "시설의 실제 위치와 이용 시간은 학교 안내도나 선생님을 통해 확인하세요."
    )


# -----------------------------
# 친구 사귀기
# -----------------------------
elif page == "🤝 친구 사귀기":
    st.title("🤝 친구 사귀기")
    st.write("처음에는 어색해도 작은 인사부터 시작하면 좋아요.")

    info_card(
        "먼저 인사하기",
        "등교할 때 가볍게 인사하면 자연스럽게 대화를 시작할 수 있어요.",
        "👋"
    )

    info_card(
        "공통 관심사 찾기",
        "좋아하는 과목, 취미, 음악 등 공통된 관심사로 이야기해 보세요.",
        "🎧"
    )

    info_card(
        "모르는 것 함께 물어보기",
        "교실 위치나 과제 내용을 함께 확인하면서 대화를 나눌 수 있어요.",
        "💬"
    )

    info_card(
        "천천히 친해지기",
        "처음부터 많은 친구를 사귀려고 부담을 갖지 않아도 괜찮아요.",
        "🌱"
    )

    st.success(
        "친구 관계는 서두르지 않아도 괜찮아요. "
        "자신에게 편안한 속도로 다가가 보세요."
    )


# -----------------------------
# 학교생활 팁
# -----------------------------
elif page == "📌 학교생활 팁":
    st.title("📌 알아두면 좋은 학교생활 팁")

    with st.expander("📅 수행평가 관리하기"):
        st.write(
            "수행평가 날짜와 제출 기한을 달력이나 메모 앱에 기록해 두세요. "
            "과목별로 정리하면 준비해야 할 일을 놓치지 않을 수 있어요."
        )

    with st.expander("🎒 가방 미리 챙기기"):
        st.write(
            "시간표를 확인한 뒤 교과서, 필기구, 과제물을 전날 준비해 두세요."
        )

    with st.expander("🙋 학교에서 도움이 필요할 때"):
        st.write(
            "학교생활 중 불편하거나 어려운 일이 있다면 "
            "담임 선생님이나 믿을 수 있는 교직원에게 도움을 요청하세요."
        )

    with st.expander("⏰ 시간 관리하기"):
        st.write(
            "등교 시간과 쉬는 시간, 수업 시작 시간을 확인하고 "
            "이동이 필요한 수업은 조금 일찍 준비해 보세요."
        )

    with st.expander("📢 공지 확인하기"):
        st.write(
            "학교 홈페이지와 학교에서 안내하는 공지를 주기적으로 확인하세요."
        )


# -----------------------------
# 유용한 링크
# -----------------------------
elif page == "🔗 유용한 링크":
    st.title("🔗 유용한 링크")
    st.write("학교생활에 도움이 되는 사이트를 모아두었어요.")

    link_card(
        "🏫 천안오성고등학교 공식 홈페이지",
        "학교 공지사항과 공식 정보를 확인할 수 있어요.",
        "http://ohsung.caehs.kr"
    )

    link_card(
        "🗓️ 시간표 확인 사이트",
        "시간표 관련 정보를 확인할 수 있어요.",
        "https://www.classroutine.net/schools/N10/8140246"
    )

    link_card(
        "🍱 급식 정보 사이트",
        "급식 메뉴 관련 정보를 확인할 수 있어요.",
        "https://school.weingchicken.com/schools/8584"
    )

    st.divider()
    st.subheader("나만의 링크 추가하기")

    with st.form("add_link_form"):
        new_title = st.text_input("링크 이름", placeholder="예: 학교에서 자주 쓰는 사이트")
        new_url = st.text_input("사이트 주소", placeholder="https://example.com")
        new_description = st.text_input(
            "간단한 설명",
            placeholder="어떤 사이트인지 적어 주세요."
        )

        submitted = st.form_submit_button("링크 추가하기")

        if submitted:
            if not new_title.strip() or not new_url.strip():
                st.error("링크 이름과 사이트 주소를 입력해 주세요.")
            elif not (
                new_url.strip().startswith("https://")
                or new_url.strip().startswith("http://")
            ):
                st.error("사이트 주소는 http:// 또는 https://로 시작해야 해요.")
            else:
                st.session_state.custom_links.append({
                    "title": new_title.strip(),
                    "url": new_url.strip(),
                    "description": new_description.strip()
                })
                st.success("링크를 추가했어요!")

    if st.session_state.custom_links:
        st.subheader("추가한 링크")

        for i, item in enumerate(st.session_state.custom_links):
            with st.container(border=True):
                st.markdown(f"### {item['title']}")
                if item["description"]:
                    st.write(item["description"])

                st.link_button("사이트 열기 ↗", item["url"])

                if st.button("이 링크 삭제", key=f"delete_link_{i}"):
                    st.session_state.custom_links.pop(i)
                    st.rerun()


# -----------------------------
# 준비물 체크리스트
# -----------------------------
elif page == "✅ 준비물 체크리스트":
    st.title("✅ 준비물 체크리스트")
    st.write("등교하기 전에 준비물을 확인해 보세요.")

    items = [
        "교과서와 학습 자료",
        "필통과 필기구",
        "과제물과 제출 서류",
        "학생증 (필요한 경우)",
        "개인 물병",
        "시간표 확인하기",
        "학교 공지 확인하기",
        "다음 날 준비물 확인하기"
    ]

    checked_count = 0

    for item in items:
        checked = st.checkbox(
            item,
            key=f"check_{item}"
        )
        if checked:
            checked_count += 1

    total = len(items)
    progress = checked_count / total

    st.divider()
    st.subheader("준비 진행 상황")

    st.progress(progress)
    st.write(f"**{checked_count} / {total}개** 준비 완료")

    if checked_count == total:
        st.success("모든 항목을 확인했어요. 내일도 힘내세요! 🎉")
    else:
        st.caption("체크하지 않은 항목을 확인하고 차근차근 준비해 보세요.")


# -----------------------------
# 하단 안내
# -----------------------------
st.divider()

st.markdown(
    "<p class='small-note'>천안오성고등학교 학교생활 길잡이 · "
    "학교의 공식 안내와 최신 공지를 우선으로 확인하세요.</p>",
    unsafe_allow_html=True
)
