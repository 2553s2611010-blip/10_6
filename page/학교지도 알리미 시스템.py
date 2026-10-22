
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="오성고 학교지도 알리미",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# 학교 시설 데이터
# 주의: 실제 학교 배치가 아닌 예시 데이터입니다.
# 실제 위치를 확인한 후 건물, 층, 위치 설명을 수정하세요.
# --------------------------------------------------
FACILITIES = [
    {
        "name": "교무실",
        "category": "교직원 시설",
        "building": "본관",
        "floor": "1층",
        "location": "위치 확인 필요",
        "description": "선생님 및 학교생활 관련 문의",
        "icon": "👩‍🏫",
    },
    {
        "name": "행정실",
        "category": "교직원 시설",
        "building": "본관",
        "floor": "1층",
        "location": "위치 확인 필요",
        "description": "학교 행정 및 서류 관련 문의",
        "icon": "📋",
    },
    {
        "name": "보건실",
        "category": "학생 편의 시설",
        "building": "본관",
        "floor": "1층",
        "location": "위치 확인 필요",
        "description": "몸이 아프거나 다쳤을 때 방문",
        "icon": "🩺",
    },
    {
        "name": "도서관",
        "category": "학습 시설",
        "building": "본관",
        "floor": "2층",
        "location": "위치 확인 필요",
        "description": "독서 및 학습 자료 이용",
        "icon": "📚",
    },
    {
        "name": "1학년 교실",
        "category": "교실",
        "building": "본관",
        "floor": "2층",
        "location": "위치 확인 필요",
        "description": "1학년 교실 위치 안내",
        "icon": "🏫",
    },
    {
        "name": "2학년 교실",
        "category": "교실",
        "building": "본관",
        "floor": "3층",
        "location": "위치 확인 필요",
        "description": "2학년 교실 위치 안내",
        "icon": "🏫",
    },
    {
        "name": "3학년 교실",
        "category": "교실",
        "building": "본관",
        "floor": "4층",
        "location": "위치 확인 필요",
        "description": "3학년 교실 위치 안내",
        "icon": "🏫",
    },
    {
        "name": "급식실",
        "category": "학생 편의 시설",
        "building": "별관",
        "floor": "1층",
        "location": "위치 확인 필요",
        "description": "식사 공간 및 급식 이용",
        "icon": "🍱",
    },
    {
        "name": "체육관",
        "category": "체육 시설",
        "building": "별관",
        "floor": "1층",
        "location": "위치 확인 필요",
        "description": "체육 수업 및 실내 활동",
        "icon": "🏀",
    },
    {
        "name": "화장실",
        "category": "학생 편의 시설",
        "building": "본관",
        "floor": "각 층",
        "location": "실제 위치 확인 필요",
        "description": "화장실 위치는 해당 층에서 확인",
        "icon": "🚻",
    },
]

# 학교에서 직접 수정할 수 있는 기본 공지
NOTICES = [
    {
        "title": "학교 지도 이용 안내",
        "date": "상시",
        "content": "시설 이름을 검색하거나 층별 필터를 이용해 보세요.",
    },
    {
        "title": "위치 정보 확인 안내",
        "date": "필독",
        "content": "현재 표시되는 시설 위치는 예시입니다. 실제 위치를 확인하세요.",
    },
    {
        "title": "안전 이용 안내",
        "date": "상시",
        "content": "이동할 때는 뛰지 말고 복도와 계단에서 안전에 유의하세요.",
    },
]

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f7fb;
    }
    .main-title {
        font-size: 2.15rem;
        font-weight: 800;
        color: #17365d;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #63738a;
        margin-bottom: 1.4rem;
    }
    .facility-card {
        background: white;
        border: 1px solid #e4eaf2;
        border-radius: 14px;
        padding: 18px;
        min-height: 155px;
        margin-bottom: 10px;
    }
    .facility-icon {
        font-size: 1.8rem;
    }
    .facility-name {
        color: #17365d;
        font-weight: 750;
        font-size: 1.1rem;
        margin: 6px 0;
    }
    .muted {
        color: #68778b;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 사이드바
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🏫 오성고 알리미")
    st.caption("천안 오성고등학교 학교 안내")
    page = st.radio(
        "메뉴",
        [
            "홈",
            "학교 시설 지도",
            "시설 검색",
            "길찾기",
            "공지사항",
        ],
    )
    st.divider()
    st.caption("학교 시설 데이터는 관리자 확인 후 수정해 주세요.")

# --------------------------------------------------
# 공통 헤더
# --------------------------------------------------
st.markdown(
    '<div class="main-title">🏫 천안 오성고등학교</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">학교 시설과 교실을 쉽고 빠르게 찾아보세요.</div>',
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 홈
# --------------------------------------------------
if page == "홈":
    st.subheader("학교 안내 대시보드")
    st.write("필요한 시설을 선택하거나 아래 메뉴에서 바로 찾아보세요.")

    c1, c2, c3 = st.columns(3)
    c1.metric("등록된 시설", f"{len(FACILITIES)}개")
    c2.metric("안내 메뉴", "5개")
    c3.metric("공지사항", f"{len(NOTICES)}개")

    st.markdown("### 🔎 빠른 검색")
    quick_query = st.text_input(
        "시설 이름 입력",
        placeholder="예: 보건실, 도서관, 급식실",
        key="home_search",
    )

    if quick_query.strip():
        matches = [
            item for item in FACILITIES
            if quick_query.strip().lower()
            in (
                item["name"]
                + item["category"]
                + item["building"]
                + item["description"]
            ).lower()
        ]
        if matches:
            for item in matches:
                with st.container(border=True):
                    st.markdown(
                        f"### {item['icon']} {item['name']}"
                    )
                    st.write(
                        f"**건물:** {item['building']} · "
                        f"**층:** {item['floor']}"
                    )
                    st.write(item["description"])
                    st.caption(f"위치: {item['location']}")
        else:
            st.info("검색 결과가 없습니다. 다른 단어로 검색해 보세요.")

    st.markdown("### ⭐ 자주 찾는 시설")
    popular_names = ["교무실", "보건실", "도서관", "급식실"]
    cols = st.columns(4)
    for col, name in zip(cols, popular_names):
        item = next(
            (x for x in FACILITIES if x["name"] == name),
            None,
        )
        if item:
            with col:
                st.markdown(
                    f"""
                    <div class="facility-card">
                        <div class="facility-icon">{item['icon']}</div>
                        <div class="facility-name">{item['name']}</div>
                        <div class="muted">{item['building']} · {item['floor']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.info(
        "안내: 현재 시설 배치는 예시입니다. "
        "실제 학교의 건물 및 교실 위치와 다를 수 있습니다."
    )

# --------------------------------------------------
# 시설 지도
# --------------------------------------------------
elif page == "학교 시설 지도":
    st.subheader("🗺️ 학교 시설 지도")
    st.write("건물과 층을 선택해 등록된 시설을 살펴보세요.")

    buildings = ["전체"] + sorted(
        set(item["building"] for item in FACILITIES)
    )
    floors = ["전체"] + sorted(
        set(item["floor"] for item in FACILITIES)
    )

    f1, f2 = st.columns(2)
    with f1:
        selected_building = st.selectbox("건물 선택", buildings)
    with f2:
        selected_floor = st.selectbox("층 선택", floors)

    filtered = [
        item for item in FACILITIES
        if (selected_building == "전체"
            or item["building"] == selected_building)
        and (selected_floor == "전체"
             or item["floor"] == selected_floor)
    ]

    if filtered:
        for start in range(0, len(filtered), 2):
            cols = st.columns(2)
            for col, item in zip(cols, filtered[start:start + 2]):
                with col:
                    with st.container(border=True):
                        st.markdown(f"## {item['icon']} {item['name']}")
                        st.caption(
                            f"{item['building']} · {item['floor']} · "
                            f"{item['category']}"
                        )
                        st.write(item["description"])
                        st.warning(f"📍 {item['location']}")
    else:
        st.info("선택한 조건에 해당하는 시설이 없습니다.")

    st.caption(
        "이 화면은 시설 목록을 이용한 안내이며 실제 건물 도면은 아닙니다."
    )

# --------------------------------------------------
# 시설 검색
# --------------------------------------------------
elif page == "시설 검색":
    st.subheader("🔍 시설 검색")
    query = st.text_input(
        "시설명 또는 키워드",
        placeholder="예: 2학년, 학습, 행정",
    )
    category_options = ["전체"] + sorted(
        set(item["category"] for item in FACILITIES)
    )
    category = st.selectbox("시설 종류", category_options)

    results = [
        item for item in FACILITIES
        if (
            not query.strip()
            or query.strip().lower() in (
                item["name"]
                + item["category"]
                + item["building"]
                + item["floor"]
                + item["description"]
            ).lower()
        )
        and (category == "전체" or item["category"] == category)
    ]

    st.caption(f"검색 결과: {len(results)}개")

    if results:
        for item in results:
            with st.container(border=True):
                left, right = st.columns([3, 1])
                with left:
                    st.markdown(f"### {item['icon']} {item['name']}")
                    st.write(item["description"])
                    st.caption(
                        f"{item['building']} · {item['floor']} · "
                        f"{item['category']}"
                    )
                with right:
                    st.write("**위치 안내**")
                    st.write(item["location"])
    else:
        st.warning("검색 결과가 없습니다. 검색어를 바꿔 보세요.")

# --------------------------------------------------
# 길찾기
# --------------------------------------------------
elif page == "길찾기":
    st.subheader("🧭 학교 안 길찾기")
    st.write("출발지와 목적지의 등록 정보를 확인합니다.")

    names = [item["name"] for item in FACILITIES]
    start_name = st.selectbox("출발 위치", names, index=0)
    end_name = st.selectbox(
        "도착할 시설",
        names,
        index=min(2, len(names) - 1),
    )

    if st.button("이동 정보 확인", type="primary"):
        start = next(
            (x for x in FACILITIES if x["name"] == start_name),
            None,
        )
        end = next(
            (x for x in FACILITIES if x["name"] == end_name),
            None,
        )

        if not start or not end:
            st.error("시설 정보를 불러오지 못했습니다.")
        elif start_name == end_name:
            st.info("출발 위치와 도착 시설이 같습니다.")
        else:
            st.markdown("### 이동 정보")
            a, b = st.columns(2)
            with a:
                st.markdown("**🚩 출발**")
                st.write(start["name"])
                st.caption(
                    f"{start['building']} · {start['floor']}"
                )
            with b:
                st.markdown("**🏁 도착**")
                st.write(end["name"])
                st.caption(
                    f"{end['building']} · {end['floor']}"
                )

            if start["building"] == end["building"]:
                st.info(
                    "같은 건물에 등록된 시설입니다. "
                    "실제 교실 위치와 복도 안내 표지를 확인하세요."
                )
            else:
                st.info(
                    "서로 다른 건물에 등록된 시설입니다. "
                    "실제 연결 통로와 출입구 위치를 확인하세요."
                )

            st.warning(
                "정확한 이동 경로와 소요 시간은 실제 도면이 등록되지 않아 "
                "제공하지 않습니다. 학교 안내 표지판을 확인하세요."
            )

# --------------------------------------------------
# 공지사항
# --------------------------------------------------
elif page == "공지사항":
    st.subheader("📢 학교 안내 및 공지사항")
    st.write("학교 이용에 필요한 안내를 확인하세요.")

    for notice in NOTICES:
        with st.container(border=True):
            st.markdown(f"### 📌 {notice['title']}")
            st.caption(f"게시 구분: {notice['date']}")
            st.write(notice["content"])

    st.caption(
        "현재 공지사항은 기본 예시입니다. "
        "실제 학교 공지를 확인한 뒤 내용을 수정하세요."
    )

st.divider()
st.caption(
    f"천안 오성고등학교 학교지도 알리미 · "
    f"화면 확인 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
)
