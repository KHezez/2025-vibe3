import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

@st.cache_data
def load_csv(url):
    return pd.read_csv(
        url,
        encoding='cp949',
        engine='python',
        on_bad_lines='skip'
    )

# —————— 원본 CSV raw URL (자신의 GitHub 주소로 변경) ——————
url1 = "https://raw.githubusercontent.com/USERNAME/REPO/main/2025년06월_연령별인구현황_월간.csv"
url2 = "https://raw.githubusercontent.com/USERNAME/REPO/main/2025년06월_연령별인구현황_월간 (1).csv"

# 데이터 로드
df1 = load_csv(url1)
df2 = load_csv(url2)

# —————— 1) 월간.csv: 광역지자체별 총인구수 & 0세 비율 ——————
# 숫자형 정리
df1['총인구수'] = df1['2025년06월_계_총인구수'].str.replace(',', '').astype(int)
df1['0세인구수'] = df1['2025년06월_계_0세'].str.replace(',', '').astype(int)
df1['0세비율(%)'] = df1['0세인구수'] / df1['총인구수'] * 100

# 레이아웃: 좌우 두 개 칼럼
c1, c2 = st.columns(2)

with c1:
    st.subheader("① 광역지자체별 총인구수")
    fig1 = px.bar(
        df1,
        x='행정구역',
        y='총인구수',
        labels={'행정구역':'지역', '총인구수':'총인구수 (명)'},
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("② 총인구 대비 0세 비율")
    fig2 = px.bar(
        df1,
        x='행정구역',
        y='0세비율(%)',
        labels={'행정구역':'지역', '0세비율(%)':'0세비율 (%)'},
        color='0세비율(%)',
        color_continuous_scale='Viridis'
    )
    fig2.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig2, use_container_width=True)

# —————— 2) 월간 (1).csv: 성별·연령대별 인구분포 ——————
st.markdown("---")
st.subheader("③ 성별·연령대별 인구분포 (월간 (1).csv)")

# 사용자에게 지역 선택하게 하기
region = st.selectbox("분석할 행정구역을 선택하세요", df2['행정구역'].unique())

# 선택된 지역 필터링
df_sel = df2[df2['행정구역'] == region].iloc[0]

# 연령구간 리스트
age_bins = ['0~9세','10~19세','20~29세','30~39세','40~49세',
            '50~59세','60~69세','70~79세','80~89세','90~99세','100세 이상']

# 남/여 인구 추출
male = []
female = []
for age in age_bins:
    male_col = f'2025년06월_남_{age}'
    female_col = f'2025년06월_여_{age}'
    male.append(int(df_sel[male_col].replace(',', '')))
    female.append(int(df_sel[female_col].replace(',', '')))

df_gender = pd.DataFrame({
    '연령대': age_bins,
    '남자': male,
    '여자': female
})

# 그룹 바차트
fig3 = px.bar(
    df_gender,
    x='연령대',
    y=['남자','여자'],
    barmode='group',
    labels={'value':'인구수 (명)','연령대':'연령대','variable':'성별'},
    title=f"{region} 성별·연령대별 인구분포"
)
fig3.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig3, use_container_width=True)
