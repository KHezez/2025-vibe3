import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd

st.title("인터랙티브 지도 데모 (Folium+Streamlit)")

# 샘플 데이터 (서울 명소)
data = pd.DataFrame({
    '장소': ['경복궁', 'N서울타워', '롯데월드타워', '여의도공원'],
    '위도': [37.579617, 37.551169, 37.513068, 37.528311],
    '경도': [126.977041, 126.988227, 127.102492, 126.924921]
})

# 지도 생성(초기 중심: 서울시청)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12, tiles='CartoDB positron')

# 마커 추가
for _, row in data.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['장소'],
        tooltip=row['장소'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# streamlit에서 folium 지도 표시(마커 클릭도 interactivity)
st.write("### 마커를 클릭하면 팝업이 나옵니다")
st_data = st_folium(m, width=700, height=500)

# 지도 클릭시 좌표 출력 (진짜 지도답게 interactivity!)
if st_data and st_data.get("last_clicked"):
    st.write("**지도 클릭 좌표:**", st_data["last_clicked"])
