
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from urllib.parse import quote

# 기본 설정
st.set_page_config(
    page_title="천안오성고 학교 지도",
    page_icon="🏫",
    layout="wide",
)

SCHOOL_NAME = "천안오성고등학교"
SCHOOL_ADDRESS = "충청남도 천안시 서북구 과수원길 27"
SCHOOL_PHONE = "041-558-3702"
SCHOOL_WEBSITE = "http://ohsung.caehs.kr"

st.markdown("""
<style>
    .main-title {
        font-size: 2.15rem;
        font-weight: 800;
        color: #193B69;
        margin-bottom: 4px;
    }
    .sub-title {
        color: #68778B;
        margin-bottom: 24px;
    }
    .info-card {
        background: #F2F6FC;
        border: 1px solid #DCE6F3;
        border-radius: 14px;
        padding: 18px;
        min-height: 105px;
    }
    .info-label {
        font-size: 0.9rem;
        color: #536780;
    }
    .info-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #193B69;
        margin-top: 8px;
    }
    div[data-testid="stMetric"] {
        background: #F2F6FC;
        padding: 14px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown("## 🏫 오성고 지도 알리미")
    st.caption("학교 위치와 시설 안내")
    page = st.radio(
        "메뉴",
        ["학교 지도", "시설 찾기", "학교 정보"],
        index=0,
    )
    st.divider()
    st.caption("천안오성고등학교")
    st.caption("충남 천안시 서북구")

# 헤더
st.markdown(
    '<div class="main-title">🏫 천안오성고등학교</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-title">학교 지도 알리미 시스템 · '
    '우리 학교 위치를 쉽고 빠르게 찾아보세요.</div>',
    unsafe_allow_html=True,
)

if page == "학교 지도":
    st.subheader("📍 학교 위치 안내")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="info-card"><div class="info-label">'
            '학교명</div><div class="info-value">'
            '천안오성고등학교</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="info-card"><div class="info-label">'
            '학교 주소</div><div class="info-value">'
            '충남 천안시 서북구</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="info-card"><div class="info-label">'
            '대표 전화</div><div class="info-value">'
            '041-558-3702</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown("### 🗺️ 학교 주변 지도")

    map_url = (
        "https://www.google.com/maps?"
        "q=" + quote(SCHOOL_NAME + " " + SCHOOL_ADDRESS)
        + "&output=embed"
    )

    try:
        components.iframe(
            map_url,
            height=430,
            scrolling=False,
        )
    except Exception:
        st.warning("지도를 표시하지 못했습니다. 아래 버튼으로 확인해 주세요.")

    st.link_button(
        "📍 지도 크게 보기 / 길찾기",
        "https://www.google.com/maps/dir/?api=1&destination="
        + quote(SCHOOL_NAME + " " + SCHOOL_ADDRESS),
        use_container_width=True,
    )

    st.info(
        "위 지도는 학교 주변 위치를 보여주는 외부 지도입니다. "
        "건물 내부의 교실 배치도와는 다릅니다."
    )

    st.markdown("### 🏢 교내 상세 배치도")
    map_file = Path("assets/school_map.png")

    if map_file.is_file():
        try:
            st.image(
                str(map_file),
                caption="천안오성고등학교 교내 배치도",
                use_container_width=True,
            )
        except Exception:
            st.warning("배치도 이미지를 불러오지 못했습니다.")
    else:
        st.warning(
            "아직 교내 상세 배치도 이미지가 등록되지 않았습니다."
        )
        st.write(
            "학교에서 받은 배치도 이미지를 "
            "`assets/school_map.png` 경로에 추가하면 표시됩니다."
        )

elif page == "시설 찾기":
    st.subheader("🔎 교내 시설 찾기")
    st.write("찾고 싶은 시설을 선택하세요.")

    facilities = {
        "교실": "수업이 진행되는 공간입니다.",
        "교무실": "교사에게 문의하거나 학교 안내를 받을 때 이용합니다.",
        "행정실": "학교 행정 관련 문의를 할 수 있는 곳입니다.",
        "도서관": "독서와 자료 검색을 위한 공간입니다.",
        "급식실": "점심 식사 등을 위한 공간입니다.",
        "체육관": "체육 활동을 위한 공간입니다.",
        "보건실": "학교에서 몸이 아프거나 다쳤을 때 도움을 요청하는 곳입니다.",
        "화장실": "교내 편의시설입니다.",
    }

    selected = st.selectbox(
        "시설 선택",
        list(facilities.keys()),
        index=0,
    )

    st.markdown("---")
    st.markdown(f"### 📌 {selected}")
    st.write(facilities[selected])

    st.info(
        "정확한 층수와 위치는 검증된 교내 배치도 자료가 "
        "등록된 후 안내할 수 있습니다. "
        "현재는 위치를 임의로 표시하지 않습니다."
    )

    if st.button("학교 위치 및 연락처 확인", use_container_width=True):
        st.write(f"주소: {SCHOOL_ADDRESS}")
        st.write(f"전화: {SCHOOL_PHONE}")
        st.link_button(
            "학교 지도 열기",
            "https://www.google.com/maps/dir/?api=1&destination="
            + quote(SCHOOL_NAME + " " + SCHOOL_ADDRESS),
        )

elif page == "학교 정보":
    st.subheader("ℹ️ 학교 기본 정보")

    st.markdown(f"**학교명:** {SCHOOL_NAME}")
    st.markdown(f"**주소:** {SCHOOL_ADDRESS}")
    st.markdown(f"**전화번호:** {SCHOOL_PHONE}")
    st.markdown("**학교 구분:** 공립 고등학교")

    st.link_button(
        "🌐 학교 홈페이지 방문",
        SCHOOL_WEBSITE,
        use_container_width=True,
    )

    st.link_button(
        "📍 학교 위치 확인",
        "https://www.google.com/maps/search/?api=1&query="
        + quote(SCHOOL_NAME + " " + SCHOOL_ADDRESS),
        use_container_width=True,
    )

    st.caption(
        "학교 정보는 변경될 수 있으니 방문 전 공식 홈페이지에서 확인하세요."
    )

st.divider()
st.caption("천안오성고등학교 지도 알리미 | 학교 위치 안내 서비스")
