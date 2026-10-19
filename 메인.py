
import streamlit as st
from urllib.parse import urlparse

st.set_page_config(
    page_title="천안오성고 새 학교 길잡이",
    page_icon="🎒",
    layout="wide",
)

st.markdown("""
<style>
.stApp {background-color: #f7f9fc;}
.block-container {max-width: 1100px; padding-top: 2rem;}
.hero {
    background: linear-gradient(120deg, #e2efff, #e6f7ed);
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 20px;
}
.hero h1 {color: #23476b;}
</style>
""", unsafe_allow_html=True)

SCHOOL = {
    "name": "천안오성고등학교",
    "address": "충청남도 천안시 서북구 과수원길 27",
    "phone": "041-558-3702",
    "website": "http://ohsung.caehs.kr",
}

LINKS = {
    "학교 홈페이지": SCHOOL["website"],
    "시간표·급식 확인": (
        "https://www.classroutine.net/schools/N10/8140246"
    ),
    "급식·시간표·학사일정": (
        "https://school.weingchicken.com/schools/8584"
    ),
}

GUIDES = {
    "학교생활": {
        "icon": "📚",
        "intro": "수업과 학교생활에 필요한 정보를 확인해요.",
        "items": {
            "시간표 확인": [
                "시간표 사이트에서 학년과 반을 선택해요.",
                "수업 과목과 교실을 확인하고 준비물을 챙겨요.",
                "시간표가 정확하지 않다면 학교 공지를 확인해요.",
            ],
            "급식 확인": [
                "급식 안내 사이트에서 날짜별 메뉴를 확인해요.",
                "알레르기가 있다면 메뉴와 알레르기 정보를 주의 깊게 살펴봐요.",
                "최신 식단은 학교의 공식 안내와 함께 확인해요.",
            ],
            "학교 공지": [
                "학교 홈페이지에서 공지사항을 확인해요.",
                "수행평가와 제출 기한을 따로 기록해 두어요.",
                "모르는 내용은 담임 선생님께 질문해요.",
            ],
        },
    },
    "학교 시설": {
        "icon": "🏫",
        "intro": "학교의 주요 시설을 이용하는 방법을 알아봐요.",
        "items": {
            "교무실": [
                "선생님을 찾아가야 할 때 교무실 위치를 확인해요.",
                "정확한 위치는 학교 안내도나 선생님께 확인해요.",
            ],
            "보건실": [
                "학교에서 몸이 아프거나 다쳤을 때 이용해요.",
                "위치를 모르면 가까운 선생님께 도움을 요청해요.",
            ],
            "도서관": [
                "도서 대출과 반납 방법을 알아봐요.",
                "운영 시간과 이용 규칙은 학교 안내를 확인해요.",
            ],
            "행정실": [
                "학교 행정 관련 문의가 있을 때 이용해요.",
                "어디에 문의해야 할지 모르겠다면 선생님께 물어봐요.",
            ],
        },
    },
    "친구 사귀기": {
        "icon": "🤝",
        "intro": "새로운 친구들과 천천히 친해져 봐요.",
        "items": {
            "먼저 인사하기": [
                "옆자리 친구에게 먼저 인사해 봐요.",
                "서로 이름을 소개하며 대화를 시작해요.",
            ],
            "대화 시작하기": [
                "수업이나 학교생활에 관해 가볍게 질문해 봐요.",
                "공통 관심사를 찾아 이야기해 봐요.",
            ],
            "도움 요청하기": [
                "교실이나 학교 규칙이 궁금하면 친구에게 물어봐요.",
                "어려운 일이 있으면 선생님에게 도움을 요청해도 괜찮아요.",
            ],
        },
    },
    "학교 규칙": {
        "icon": "📋",
        "intro": "학교생활에 필요한 규칙을 확인해요.",
        "items": {
            "등교와 출결": [
                "등교 시간과 출결 처리 방법을 확인해요.",
                "지각이나 결석 시 필요한 절차를 알아봐요.",
            ],
            "교실 생활": [
                "수업 시간과 쉬는 시간의 규칙을 지켜요.",
                "교실과 공용 공간을 깨끗하게 사용해요.",
            ],
            "공지 확인": [
                "학교에서 전달하는 공지사항을 자주 확인해요.",
                "학교의 공식 생활 규정을 기준으로 행동해요.",
            ],
        },
    },
}


def valid_url(url):
    try:
        parsed = urlparse(url.strip())
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
            and " " not in url.strip()
        )
    except (ValueError, AttributeError):
        return False


if "page" not in st.session_state:
    st.session_state.page = "홈"

if "custom_links" not in st.session_state:
    st.session_state.custom_links = []

if "checked_tasks" not in st.session_state:
    st.session_state.checked_tasks = {}

menu = [
    "홈",
    "학교생활",
    "학교 시설",
    "친구 사귀기",
    "학교 규칙",
    "안내 링크 관리",
    "적응 체크리스트",
]

with st.sidebar:
    st.title("🎒 오성고 길잡이")
    st.caption("천안오성고등학교 전학생 안내")
    st.divider()

    selected = st.radio(
        "메뉴 선택",
        menu,
        index=menu.index(st.session_state.page)
        if st.session_state.page in menu else 0,
    )
    st.session_state.page = selected

    st.divider()
    st.caption("학교의 최신 공식 안내를 함께 확인하세요.")


def show_links():
    st.subheader("🔗 유용한 학교 사이트")

    for name, url in LINKS.items():
        st.link_button(
            name + " ↗",
            url,
            use_container_width=True,
        )

    for i, item in enumerate(st.session_state.custom_links):
        st.link_button(
            item["name"] + " ↗",
            item["url"],
            use_container_width=True,
            key=f"custom_link_{i}",
        )


if selected == "홈":
    st.markdown("""
    <div class="hero">
        <h1>천안오성고등학교에 온 걸 환영해요! 🎉</h1>
        <p>새로운 학교생활이 낯설어도 괜찮아요.</p>
        <p>수업, 학교 시설, 친구 관계에 필요한 정보를 찾아봐요.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🏫 우리 학교 정보")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("학교", SCHOOL["name"])
        st.write("📍 " + SCHOOL["address"])
    with col2:
        st.write("☎️ 대표 전화")
        st.write(SCHOOL["phone"])
        st.link_button(
            "공식 홈페이지 방문 ↗",
            SCHOOL["website"],
            use_container_width=True,
        )

    st.divider()
    st.subheader("무엇이 필요하세요?")

    cards = list(GUIDES.items())
    for i in range(0, len(cards), 2):
        columns = st.columns(2)

        for col, (name, data) in zip(columns, cards[i:i + 2]):
            with col:
                with st.container(border=True):
                    st.subheader(f"{data['icon']} {name}")
                    st.write(data["intro"])

                    if st.button(
                        "안내 보기",
                        key=f"go_{name}",
                        use_container_width=True,
                    ):
                        st.session_state.page = name
                        st.rerun()

    show_links()

elif selected in GUIDES:
    data = GUIDES[selected]

    st.title(f"{data['icon']} {selected}")
    st.write(data["intro"])

    for section, tips in data["items"].items():
        with st.expander(section):
            for tip in tips:
                st.write("• " + tip)

    if selected == "학교생활":
        show_links()

    st.info(
        "시설 위치와 세부 규칙은 학교의 최신 공식 안내를 확인하세요."
    )

elif selected == "안내 링크 관리":
    st.title("🔗 안내 링크 관리")
    st.write("학교생활에 필요한 웹페이지를 추가할 수 있어요.")

    with st.form("link_form", clear_on_submit=True):
        name = st.text_input("페이지 이름")
        url = st.text_input(
            "페이지 주소",
            placeholder="https://example.com",
        )
        submitted = st.form_submit_button("링크 추가")

        if submitted:
            name = name.strip()
            url = url.strip()

            if not name:
                st.error("페이지 이름을 입력해 주세요.")
            elif not valid_url(url):
                st.error("올바른 HTTP 또는 HTTPS 주소를 입력해 주세요.")
            elif any(
                item["url"] == url
                for item in st.session_state.custom_links
            ):
                st.warning("이미 등록된 주소예요.")
            else:
                st.session_state.custom_links.append(
                    {"name": name, "url": url}
                )
                st.success("링크를 추가했어요!")
                st.rerun()

    st.subheader("기본 제공 링크")
    show_links()

    st.caption(
        "직접 추가한 링크는 현재 세션에 저장됩니다. "
        "앱을 다시 시작하면 사라질 수 있어요."
    )

elif selected == "적응 체크리스트":
    st.title("✅ 나의 오성고 적응 체크리스트")
    st.write("확인한 항목을 체크해 보세요.")

    tasks = [
        "학교 홈페이지와 공지사항 확인하기",
        "시간표와 교과서 확인하기",
        "급식실 위치와 식단 확인하기",
        "담임 선생님과 주요 연락 방법 알아보기",
        "보건실과 교무실 위치 알아보기",
        "학교 규칙과 출결 방법 확인하기",
        "반 친구에게 먼저 인사해 보기",
        "수행평가와 제출 기한 기록하기",
    ]

    count = sum(
        st.session_state.checked_tasks.get(task, False)
        for task in tasks
    )

    st.progress(count / len(tasks))
    st.write(f"완료한 항목: **{count}/{len(tasks)}**")

    for task in tasks:
        st.session_state.checked_tasks[task] = st.checkbox(
            task,
            value=st.session_state.checked_tasks.get(task, False),
            key=f"check_{task}",
        )

    if count == len(tasks):
        st.success("모든 항목을 확인했어요! 새로운 학교생활을 응원해요 🎉")

st.divider()
st.caption(
    "천안오성고 새 학교 길잡이 | 학교 공식 공지와 최신 정보를 기준으로 이용하세요."
)
