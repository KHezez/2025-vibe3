import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🎬 영화 평점/흥행 대시보드")

# 1. 파일 업로드
uploaded_file = st.file_uploader("영화 데이터(.csv) 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 2. 장르/연도 필터
    all_genres = sorted(set(sum([str(g).split(', ') for g in df['genre'].dropna()], [])))
    sel_genres = st.multiselect("장르 선택", all_genres, default=all_genres[:3])
    sel_years = st.slider("연도 범위", int(df['year'].min()), int(df['year'].max()), (2000, 2023))

    # 3. 필터 적용
    filtered = df[
        df['year'].between(*sel_years) &
        df['genre'].apply(lambda g: any(gen in str(g) for gen in sel_genres))
    ]

    st.write(f"선택된 영화 수: {len(filtered)}")

    # 4. 평점 분포 (히스토그램)
    st.subheader("평점 분포")
    fig, ax = plt.subplots()
    ax.hist(filtered['rating'].dropna(), bins=20, color='skyblue', edgecolor='gray')
    ax.set_xlabel("평점")
    ax.set_ylabel("영화 수")
    st.pyplot(fig)

    # 5. TOP 10 평점 영화
    st.subheader("TOP 10 평점 영화")
    top10 = filtered.sort_values('rating', ascending=False).head(10)
    st.dataframe(top10[['title', 'year', 'genre', 'rating', 'revenue_millions']])

    # 6. TOP 5 수익 영화
    st.subheader("TOP 5 흥행 영화 (수익)")
    top5_rev = filtered.sort_values('revenue_millions', ascending=False).head(5)
    st.dataframe(top5_rev[['title', 'year', 'revenue_millions', 'rating']])

    # 7. 연도별 평균 평점 (트렌드)
    st.subheader("연도별 평균 평점")
    trend = filtered.groupby('year')['rating'].mean()
    fig2, ax2 = plt.subplots()
    trend.plot(ax=ax2, marker='o', color='orange')
    ax2.set_ylabel("평균 평점")
    ax2.set_xlabel("연도")
    st.pyplot(fig2)

    # 8. 원하는 영화명 검색
    st.subheader("영화명으로 검색")
    keyword = st.text_input("영화 제목의 일부를 입력하세요")
    if keyword:
        res = filtered[filtered['title'].str.contains(keyword, case=False, na=False)]
        st.dataframe(res[['title', 'year', 'genre', 'rating', 'revenue_millions']])
else:
    st.info("예시용 csv 샘플: [movies_metadata.csv 다운로드](https://raw.githubusercontent.com/justmarkham/DAT8/master/data/u.item)")
