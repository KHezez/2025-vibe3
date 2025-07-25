# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ————————————————————————————————
# 1) GitHub raw URL 설정
#    자신의 레포(raw) URL로 바꿔주세요!
URL_TOTAL = "https://github.com/KHezez/2025-vibe3/blob/main/%EA%B3%84.csv"
URL_MF    = "https://raw.githubusercontent.com/USERNAME/blob/main/남여구분.csv"

# 2) 데이터 로드
df_total = pd.read_csv(URL_TOTAL, encoding='cp949')
df_mf    = pd.read_csv(URL_MF,    encoding='cp949')

# 3) 연령 컬럼이 문자열이라면 정수형으로 변환 (optional)
df_total['연령'] = df_total['연령'].astype(int)
df_mf   ['연령'] = df_mf   ['연령'].astype(int)

# 4) Streamlit 레이아웃
st.title("🧮 연령별 인구 현황")

# ————————————————————————————————
# 5) 총인구수 그래프
st.subheader("연령별 총인구수")
fig_total = px.bar(
    df_total,
    x="연령",
    y="계",
    labels={"연령":"연령 (세)", "계":"총인구수"},
    title="2025년 6월 연령별 총인구수"
)
fig_total.update_layout(xaxis_tickmode="linear")
st.plotly_chart(fig_total, use_container_width=True)

# ————————————————————————————————
# 6) 성별(남/여) 인구수 그래프
st.subheader("연령별 성별 인구수")
# melt 해서 long-form으로 변환
df_m = df_mf.melt(
    id_vars="연령",
    value_vars=["남", "여"],
    var_name="성별",
    value_name="인구수"
)
fig_mf = px.bar(
    df_m,
    x="연령",
    y="인구수",
    color="성별",
    barmode="group",
    labels={"연령":"연령 (세)", "인구수":"인구수", "성별":"성별"},
    title="2025년 6월 연령별 남녀 인구 비교"
)
fig_mf.update_layout(xaxis_tickmode="linear")
st.plotly_chart(fig_mf, use_container_width=True)

# ————————————————————————————————
# 7) 상세 데이터 보기
if st.checkbox("원본 데이터 보기"):
    st.write("■ 연령별 총인구수", df_total)
    st.write("■ 연령별 남여구분", df_mf)
