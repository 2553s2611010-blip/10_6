import streamlit as st
from datetime import date, datetime
from urllib.parse import urlparse

SCHOOL_NAME = "천안오성고등학교"
OFFICIAL_URL = "http://ohsung.caehs.kr"

st.set_page_config(
    page_title=f"{SCHOOL_NAME} 공지 알리미",
    page_icon="🏫",
    layout="wide",
)

st.title(f"🏫 {SCHOOL_NAME} 공지 알리미")
st.caption("학교 소식을 빠르게 확인하세요.")

if "notices" not in st.session_state:
    st.session_state.notices = []

query = st.text_input("공지 검색", placeholder="공지 제목 검색")

if st.button("학교 공식 홈페이지 열기"):
    st.link_button("학교 홈페이지", OFFICIAL_URL)

for notice in st.session_state.notices:
    if query.casefold() in notice["title"].casefold():
        st.subheader(notice["title"])
        st.write(notice["content"])
