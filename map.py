import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(layout="wide")

# 지도 만들기
if "markers" not in st.session_state:
    st.session_state.markers = []

m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 지도 클릭 시 위도·경도 실시간 반영
st.write("지도에서 위치를 클릭해보세요. (아래에서 마커 입력/수정 가능)")
st_data = st_folium(m, width=900, height=650)

lat, lon = 37.5665, 126.9780
if st_data and st_data.get("last_clicked"):
    lat = st_data["last_clicked"]["lat"]
    lon = st_data["last_clicked"]["lng"]

col1, col2 = st.columns([1,1])
with col1:
    lat = st.number_input("위도", value=lat, format="%.6f", key="lat_box")
with col2:
    lon = st.number_input("경도", value=lon, format="%.6f", key="lon_box")

# 마커 입력 폼
title = st.text_input("마커 제목", value="장소")
desc = st.text_input("설명 (마우스 올리면 나옴)", value="설명을 입력하세요.")

if st.button("마커 추가"):
    st.session_state.markers.append({
        "lat": lat,
        "lon": lon,
        "title": title,
        "desc": desc,
    })

# 마커 추가 (지도 다시 그림)
m = folium.Map(location=[lat, lon], zoom_start=12)
for marker in st.session_state.markers:
    folium.Marker(
        location=[marker["lat"], marker["lon"]],
        tooltip=f"<b style='font-size:18px'>{marker['title']}</b>",
        popup=marker["desc"],
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

st_folium(m, width=900, height=650)
