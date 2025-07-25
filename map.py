import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster, MeasureControl, HeatMap
import pandas as pd

st.title("프로 지도앱: 클러스터+거리재기+히트맵")

# 샘플 데이터 (대충 서울시내 100개)
data = pd.DataFrame({
    "장소": [f"spot{i}" for i in range(100)],
    "위도": 37.55 + 0.05 * np.random.rand(100),
    "경도": 126.90 + 0.07 * np.random.rand(100)
})

# 지도 생성
m = folium.Map(location=[37.57, 126.98], zoom_start=11, tiles='Stamen Terrain')

# [1] 클러스터 추가
cluster = MarkerCluster().add_to(m)
for _, row in data.iterrows():
    folium.Marker([row['위도'], row['경도']], popup=row['장소']).add_to(cluster)

# [2] 거리/면적 재기
m.add_child(MeasureControl())

# [3] 히트맵 추가
HeatMap(data[["위도", "경도"]], radius=15, blur=7, min_opacity=0.2).add_to(m)

st_folium(m, width=800, height=600)
