import streamlit as st
from streamlit_folium import st_folium
import folium
import time

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align:center;font-size:52px;'>🧷</h1>", unsafe_allow_html=True)
st.write("**핀 이모지를 드래그한다고 상상하고, 지도 원하는 곳을 클릭하세요! (가상 핀 드롭 효과)**")

# 세션상태로 애니메이션/위치 관리
if "pin_dropped" not in st.session_state:
    st.session_state.pin_dropped = False
    st.session_state.pin_lat = None
    st.session_state.pin_lon = None

m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

st_data = st_folium(m, width=900, height=650)

# 지도 클릭하면 "핀 드롭 연출"
if st_data and st_data.get("last_clicked"):
    st.session_state.pin_lat = st_data["last_clicked"]["lat"]
    st.session_state.pin_lon = st_data["last_clicked"]["lng"]
    st.session_state.pin_dropped = True

# 떨어지는 애니메이션(흉내)
if st.session_state.pin_dropped:
    for size in range(110, 34, -14):
        st.markdown(
            f"<div style='position:absolute;left:47vw;top:23vh;font-size:{size}px;'>🧷</div>",
            unsafe_allow_html=True)
        time.sleep(0.08)
        st.empty()
    st.session_state.pin_dropped = False
    st.success(f"핀 위치 저장됨! (위도: {st.session_state.pin_lat:.6f}, 경도: {st.session_state.pin_lon:.6f})")
    lat = st.session_state.pin_lat
    lon = st.session_state.pin_lon
else:
    lat, lon = 37.5665, 126.9780

lat = st.number_input("위도", value=lat, format="%.6f", key="lat_box")
lon = st.number_input("경도", value=lon, format="%.6f", key="lon_box")

# 마커 추가
if st.button("해당 위치에 마커 추가"):
    m = folium.Map(location=[lat, lon], zoom_start=12)
    folium.Marker(
        location=[lat, lon],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)
    st_folium(m, width=900, height=650)
