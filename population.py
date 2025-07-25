import streamlit as st
import pandas as pd
import plotly.express as px

# GitHub raw URL (USERNAME/REPO 부분만 바꿔주세요)
URL_TOTAL = "https://raw.githubusercontent.com/USERNAME/blob/main/계.csv"
URL_MF    = "https://raw.githubusercontent.com/USERNAME/blob/main/남여구분.csv"

# UTF-8로 읽기 (또는 encoding 인자 생략)
df_total = pd.read_csv(URL_TOTAL, encoding='utf-8')
df_mf    = pd.read_csv(URL_MF,    encoding='utf-8')

# 연령 컬럼 정수형 변환
df_total['연령'] = df_total['연령'].astype(int)
df_mf   ['연령'] = df_mf   ['연령'].astype(int)

st.title("🧮 연령별 인구 현황")

# 총인구수 막대그래프
st.subheader("연령별 총인구수")
fig_total = px.bar(
    df_total,
    x="연령", y="계",
    labels={"연령":"연령 (세)", "계":"총인구수"},
    title="2025년 6월 연령별 총인구수"
)
fig_total.update_layout(xaxis_tickmode="linear")
st.plotly_chart(fig_total, use_container_width=True)

# 성별 인구수 그룹바
st.subheader("연령별 성별 인구수")
df_m = df_mf.melt("연령", value_vars=["남","여"], var_name="성별", value_name="인구수")
fig_mf = px.bar(
    df_m, x="연령", y="인구수", color="성별", barmode="group",
    labels={"연령":"연령 (세)", "인구수":"인구수", "성별":"성별"},
    title="2025년 6월 연령별 남녀 인구 비교"
)
fig_mf.update_layout(xaxis_tickmode="linear")
st.plotly_chart(fig_mf, use_container_width=True)

if st.checkbox("원본 데이터 보기"):
    st.write(df_total)
    st.write(df_mf)
