import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# 예제 데이터
df = pd.DataFrame({
    '장소': ['A', 'B', 'C'],
    '위도': [37.5, 37.6, 37.65],
    '경도': [127.0, 127.1, 127.05]
})

# 각 장소별 방문 데이터 (임의)
visit = {
    'A': [10, 23, 45, 21],
    'B': [5, 31, 15, 9],
    'C': [19, 8, 30, 12]
}
hours = ["09시", "12시", "15시", "18시"]

m = folium.Map(location=[37.6, 127.05], zoom_start=11)
for i, row in df.iterrows():
    folium.Marker(
        [row['위도'], row['경도']],
        popup=f"<b>{row['장소']}</b>",
        tooltip=row['장소'],
    ).add_to(m)

st.write("지도에서 마커 클릭 후, 아래에서 해당 장소를 선택하면 시간별 그래프가 나옵니다.")
st_data = st_folium(m, width=700, height=500)

selected = st.selectbox("장소 선택", df['장소'])
st.plotly_chart(px.bar(x=hours, y=visit[selected], labels={'x':'시간', 'y':'방문자수'}, title=f"{selected} 시간별 방문자수"))
