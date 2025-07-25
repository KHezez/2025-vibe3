# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("연령별 인구 현황 (2025년 6월) 시각화")

# 1) CSV 파일 업로드 또는 기본 파일 로드
uploaded = st.file_uploader("CSV 파일 업로드 (CP949 인코딩)", type="csv")
if uploaded:
    df = pd.read_csv(uploaded, encoding='cp949', engine='python', on_bad_lines='skip')
else:
    df = pd.read_csv(
        '/mnt/data/202506_202506_연령별인구현황_월간.csv',
        encoding='cp949', engine='python', on_bad_lines='skip'
    )

# 2) 숫자형 컬럼 전처리 (쉼표 제거 → 정수)
df['총인구수'] = df['2025년06월_계_총인구수'].str.replace(',', '').astype(int)
df['0세인구']   = df['2025년06월_계_0세'].str.replace(',', '').astype(int)

# 3) 광역지자체별 총인구수 막대그래프
st.header("광역지자체별 총인구수")
fig1 = px.bar(
    df,
    x='행정구역',
    y='총인구수',
    labels={'행정구역':'지역','총인구수':'총인구수 (명)'},
)
fig1.update_layout(title_text="2025년 6월 광역지자체별 총인구수", xaxis_tickangle=-45)
st.plotly_chart(fig1, use_container_width=True)

# 4) 총인구수 대비 0세 인구수 산점도
st.header("총인구수 대비 0세 인구수 분포")
fig2 = px.scatter(
    df,
    x='총인구수',
    y='0세인구',
    text='행정구역',
    labels={'총인구수':'총인구수 (명)','0세인구':'0세 인구수 (명)'},
)
fig2.update_traces(textposition='top center')
fig2.update_layout(title_text="광역지자체별 총인구수 vs 0세 인구수")
st.plotly_chart(fig2, use_container_width=True)

# 5) 데이터 요약표 (선택)
if st.checkbox("데이터 통계 요약 보기"):
    st.subheader("기본 통계 정보")
    st.write(df.describe())
