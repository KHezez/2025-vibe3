import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(layout="wide")

# 마커 저장
if "markers" not in st.session_state:
    st.session_state.markers = []

# 지도 클릭시 위치 저장
clicked_lat, clicked_lon = 37.5665, 126.9780  # 서울 기본값
st.write("지도 클릭 → 위치 자동 입력 → 제목·설명 작성 → '마커 추가' 누르면 지도에 핀 추가!")

m = folium.Map(location=[clicked_lat, clicked_lon], zoom_start=12)

st_data = st_folium(m, width=900, height=650)
if st_data and st_data.get("last_clicked"):
    clicked_lat = st_data["last_clicked"]["lat"]
    clicked_lon = st_data["last_clicked"]["lng"]

# 입력란
col1, col2 = st.columns([1,1])
with col1:
    lat = st.number_input("위도", value=clicked_lat, format="%.6f", key="lat_box")
with col2:
    lon = st.number_input("경도", value=clicked_lon, format="%.6f", key="lon_box")
title = st.text_input("마커 제목", value="장소", key="title_box")
desc = st.text_input("설명 (마우스 올리면 나옴)", value="설명을 입력하세요.", key="desc_box")

# 마커 추가 버튼
if st.button("마커 추가"):
    st.session_state.markers.append({
        "lat": lat,
        "lon": lon,
        "title": title,
        "desc": desc,
    })

# 지도 다시 그리기 + 마커 표시
m = folium.Map(location=[lat, lon], zoom_start=12)
for marker in st.session_state.markers:
    folium.Marker(
        location=[marker["lat"], marker["lon"]],
        tooltip=f"<b style='font-size:18px'>{marker['title']}</b>",
        popup=marker["desc"],
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)
st_folium(m, width=900, height=650)
