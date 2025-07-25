import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

st.title("데이터 분석 & 지도 + 인터랙티브 그래프 웹앱")

uploaded = st.file_uploader("CSV 파일을 업로드하세요 (위도, 경도 포함)", type="csv")

if uploaded:
    df = pd.read_csv(uploaded)
    st.write("#### 원본 데이터", df.head())

    # 좌표 컬럼 자동 감지
    lat_col = [c for c in df.columns if 'lat' in c.lower()][0]
    lon_col = [c for c in df.columns if 'lon' in c.lower() or 'lng' in c.lower()][0]

    # pydeck 지도
    st.write("#### 지도 시각화")
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=df[lat_col].mean(),
            longitude=df[lon_col].mean(),
            zoom=11,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position=f'[{lon_col}, {lat_col}]',
                get_color='[200, 30, 0, 180]',
                get_radius=90,
            ),
        ],
    ))

    # Plotly 그래프 (숫자형 컬럼만 자동으로)
    num_cols = df.select_dtypes(include='number').columns.tolist()
    if len(num_cols) >= 2:
        st.write("#### Plotly 산점도 (첫번째/두번째 숫자형 컬럼)")
        st.plotly_chart(
            px.scatter(df, x=num_cols[0], y=num_cols[1], color=num_cols[0])
        )

    # 컬럼 선택해서 히스토그램
    col = st.selectbox("히스토그램으로 볼 컬럼", num_cols)
    st.plotly_chart(px.histogram(df, x=col))

    st.write("#### 데이터 통계 요약")
    st.write(df.describe())
else:
    st.info("CSV 파일을 업로드하면 데이터 분석, 지도, 그래프가 바로 나옵니다.")
