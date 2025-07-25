import streamlit as st
from streamlit_folium import st_folium
import folium
import time

st.set_page_config(layout="wide")

if "dropping" not in st.session_state:
    st.session_state.dropping = False

if "pin_latlon" not in st.session_state:
    st.session_state.pin_latlon = None

# 지도 만들기
center = [37.5665, 126.9780]
m = folium.Map(location=center, zoom_start=12)

st.markdown("### 📍 핀 툴: 아래 버튼을 누르고, 지도 위 아무 곳이나 클릭하면 핀이 '떨어집니다'")

col1, col2 = st.columns([2, 8])
with col1:
    if st.button("📍 핀 찍기 (드래그/드롭 느낌)", use_container_width=True):
        st.session_state.dropping = True

st_data = st_folium(m, width=900, height=650)

lat, lon = center

# dropping 모드면: 지도 클릭 좌표 체크
if st.session_state.dropping and st_data and st_data.get("last_clicked"):
    lat = st_data["last_clicked"]["lat"]
    lon = st_data["last_clicked"]["lng"]
    st.session_state.pin_latlon = (lat, lon)

    # 핀 떨어지는 애니메이션(간이, 실제로 움직이진 않지만)
    for s in range(36, 8, -3):
        st_folium(
            m,
            width=900,
            height=650,
            key=f"pin_{s}"
        )
        st.markdown(
            f"<div style='font-size:{s}px;position:absolute;left:60%;top:40%;transform:translate(-50%, -50%);'>📍</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.04)
    st.session_state.dropping = False
    st.success(f"핀 좌표 선택됨: 위도 {lat:.6f}, 경도 {lon:.6f}")

# 선택된 핀 위치 표시(입력란)
if st.session_state.pin_latlon:
    lat, lon = st.session_state.pin_latlon
    st.write(f"**선택된 좌표:** 위도 {lat:.6f}, 경도 {lon:.6f}")

    # 이후 원하는 마커 추가 폼/기능 구현 가능 (title/desc 등)
