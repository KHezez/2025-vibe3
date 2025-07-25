import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.sidebar.title("데이터 선택")
dataset = st.sidebar.selectbox("👀 볼 데이터", ["계", "남여구분"])

if dataset == "계":
    # 전체 인구 데이터 불러오기
    df = pd.read_csv("계.csv", encoding="cp949")
    # '총인구수' 컬럼 자동 탐색 및 숫자 변환
    tot_col = [c for c in df.columns if "총인구수" in c][0]
    df["총인구수"] = df[tot_col].str.replace(",", "").astype(int)
    # 지역명 컬럼 (대부분 두번째 컬럼)
    region_col = df.columns[1]
    # Plotly 막대그래프
    fig = px.bar(
        df,
        x=region_col,
        y="총인구수",
        title="전국/광역지자체별 총인구수",
        labels={region_col: "지역", "총인구수": "총인구수 (명)"}
    )
    fig.update_layout(xaxis_tickangle=-45, margin=dict(t=50, b=0))
    st.plotly_chart(fig, use_container_width=True)

else:
    # 남녀 구분 데이터 불러오기
    df = pd.read_csv("남여구분.csv", encoding="cp949")
    # '남자', '여자' 컬럼 자동 탐색 및 숫자 변환
    male_col = [c for c in df.columns if "남자" in c][0]
    female_col = [c for c in df.columns if "여자" in c][0]
    df["남자인구"] = df[male_col].str.replace(",", "").astype(int)
    df["여자인구"] = df[female_col].str.replace(",", "").astype(int)
    region_col = df.columns[1]
    # 그룹 바차트
    fig = px.bar(
        df,
        x=region_col,
        y=["남자인구", "여자인구"],
        barmode="group",
        title="전국/광역지자체별 남녀 인구수",
        labels={region_col: "지역", "value": "인구수 (명)", "variable": "성별"}
    )
    fig.update_layout(xaxis_tickangle=-45, margin=dict(t=50, b=0))
    st.plotly_chart(fig, use_container_width=True)
