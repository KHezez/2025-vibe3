import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("인구 피라미드 대시보드")

남여 = st.file_uploader("남여구분.csv 업로드", type="csv")
합계 = st.file_uploader("계.csv 업로드 (선택)", type="csv")

if 남여:
    df = pd.read_csv(남여)
    st.write("데이터 미리보기", df.head())

    # 컬럼명 자동 감지
    colnames = df.columns.tolist()
    region_col = [c for c in colnames if "시" in c or "구" in c or "군" in c or "지역" in c][0]
    age_col = [c for c in colnames if "세" in c or "연령" in c][0]
    male_col = [c for c in colnames if "남" in c][0]
    female_col = [c for c in colnames if "여" in c][0]

    # 시군구(지역) 선택
    regions = df[region_col].unique().tolist()
    selected = st.selectbox("지역 선택", regions)

    # 해당 지역 필터
    dff = df[df[region_col] == selected].copy()
    dff = dff.sort_values(age_col)

    # 피라미드용 데이터 추출
    age = dff[age_col].astype(str)
    male = -dff[male_col].astype(int)   # 왼쪽(음수)로
    female = dff[female_col].astype(int)  # 오른쪽(양수)로

    # 피라미드 그리기
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=age, x=male, name="남자", orientation="h", marker_color="#1f77b4"
    ))
    fig.add_trace(go.Bar(
        y=age, x=female, name="여자", orientation="h", marker_color="#FFB6C1"
    ))
    fig.update_layout(
        barmode="relative",
        title=f"{selected} 연령대별 인구 피라미드",
        xaxis=dict(title="인구수", tickvals=[min(male), 0, max(female)]),
        yaxis=dict(title="연령대"),
        height=600,
        plot_bgcolor="white",
    )
    st.plotly_chart(fig, use_container_width=True)

    # 계.csv도 참고로 보여줌
    if 합계:
        df_sum = pd.read_csv(합계)
        st.write("계.csv 미리보기", df_sum.head())
else:
    st.info("남여구분.csv 파일을 업로드하세요.")
