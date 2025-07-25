import streamlit as st
from streamlit_folium import st_folium
import folium
st.title ('6줄컷 지도')
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 서울시청 기준
st_folium(m, width=800, height=600)
