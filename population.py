import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 업로드
uploaded = st.file_uploader("CSV 업로드", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    st.write(df.head())

    # melt로 연령별 피벗
    value_vars = [col for col in df.columns if "세" in col or "계" in col]  # 연령/총합 컬럼 자동 추출
    df_melt = df.melt(id_vars=[col for col in df.columns if col not in value_vars],
                      value_vars=value_vars,
                      var_name="연령대", value_name="인구수")

    # 연령대별 변화 그래프
    st.plotly_chart(
        px.line(df_melt, x="년도", y="인구수", color="연령대",
                title="년도별 연령대별 인구 변화")
    )

    # 월별 연령 구조 히트맵 등 추가 가능
else:
    st.info("CSV를 업로드하세요.")
