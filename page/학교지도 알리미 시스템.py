
import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import quote

st.set_page_config(
    page_title="천안오성고 학교지도 알리미",
    page_icon="🏫",
    layout="wide",
)

SCHOOL_NAME = "천안오성고등학교"
ADDRESS = "충청남도 천안시 서북구 과수원길 27"

st.markdown("""
<style>
.stApp { background: #f4f7fb; }
h1, h2, h3 { color: #183b63; }
</style>
""", unsafe_allow_html=True)

st.title("🏫 천안오성고등학교")
st.subheader("학교지도 알리미")
st.write("학교 위치를 확인하고 시설 정보를 찾아보세요.")

st.info(f"📍 학교 주소: {ADDRESS}")

# 실제 학교 위치 지도
map_url = (
    "https://maps.google.com/maps?"
    f"q={quote(SCHOOL_NAME + ' ' + ADDRESS)}"
    "&output=embed"
)

st.markdown("## 🗺️ 오성고등학교 위치 지도")

try:
    components.iframe(
        map_url,
        height=480,
        scrolling=False,
    )
except Exception:
    st.warning("지도를 불러오지 못했습니다. 아래 링크를 이용하세요.")

st.link_button(
    "📍 Google 지도에서 학교 보기",
    "https://www.google.com/maps/search/?api=1&query="
    + quote(SCHOOL_NAME + " " + ADDRESS),
    use_container_width=True,
)

st.divider()

st.markdown("## 🔎 학교 시설 찾기")

facilities = {
    "교무실": "학교 선생님 및 교무 관련 문의",
    "행정실": "학교 행정 및 서류 관련 문의",
    "보건실": "건강 관련 도움을 받을 수 있는 시설",
    "도서관": "독서와 학습을 위한 시설",
    "급식실": "식사를 위한 시설",
    "체육관": "체육 활동을 위한 시설",
    "운동장": "야외 체육 활동 공간",
    "화장실": "화장실 위치 확인",
}

keyword = st.text_input(
    "찾고 싶은 시설을 입력하세요",
    placeholder="예: 보건실, 도서관",
)

if keyword.strip():
    results = [
        (name, description)
        for name, description in facilities.items()
        if keyword.strip().lower() in
        (name + description).lower()
    ]
else:
    results = list(facilities.items())

if results:
    cols = st.columns(2)
    for i, (name, description) in enumerate(results):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"### 📌 {name}")
                st.write(description)
                st.caption("정확한 내부 위치는 학교에서 확인해야 합니다.")
else:
    st.warning("검색 결과가 없습니다. 다른 시설명을 입력해 보세요.")

st.divider()

st.markdown("## 🧭 학교 찾아가기")
st.write("학교 위치와 외부 이동 경로를 확인할 수 있습니다.")

st.link_button(
    "길찾기 열기",
    "https://www.google.com/maps/dir/?api=1&destination="
    + quote(SCHOOL_NAME + " " + ADDRESS),
    use_container_width=True,
)

st.caption(
    "안내: 지도는 학교의 실제 위치를 표시합니다. "
    "시설 검색 목록은 안내용이며, 내부 배치도는 아닙니다."
)
