import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 CSV/ITEM/TSV 데이터 자동 인코딩+시각화 대시보드")

file = st.file_uploader("데이터 파일 업로드", type=["csv", "tsv", "item", "dat"])

def smart_read_csv(file, sep=',', header='infer', names=None, nrows=None):
    for enc in ['utf-8', 'cp949', 'euc-kr', 'latin1']:
        try:
            df = pd.read_csv(file, sep=sep, encoding=enc, header=header, names=names, nrows=nrows)
            return df
        except UnicodeDecodeError:
            file.seek(0)
            continue
        except Exception as e:
            file.seek(0)
            continue
    raise Exception("지원하는 인코딩이 없습니다!")

if file:
    # 구분자 자동 추정
    if file.name.endswith('.tsv'):
        sep = '\t'
    elif file.name.endswith('.item') or file.name.endswith('.dat'):
        sep = '|'
    else:
        sep = ','

    st.write(f"자동 감지된 구분자: `{sep}`")
    sep = st.text_input("구분자 입력(예: , | \\t)", sep)

    # 헤더 유무
    header_opt = st.radio("첫 줄이 헤더(컬럼명)?", ["예", "아니오"], horizontal=True)
    if header_opt == "예":
        df = smart_read_csv(file, sep=sep)
    else:
        preview = smart_read_csv(file, sep=sep, header=None, nrows=1)
        st.write("첫 줄 미리보기:", preview)
        cols = st.text_input("컬럼명 콤마(,)로 입력", ",".join([f"col{i+1}" for i in range(len(preview.columns))]))
        df = smart_read_csv(file, sep=sep, header=None, names=cols.split(','))

    st.dataframe(df.head(30))

    # 컬럼 자동 분류
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    nonnum_cols = df.select_dtypes(exclude='number').columns.tolist()

    # 1. 히스토그램(숫자열)
    if numeric_cols:
        st.subheader("히스토그램 / 분포")
        col1 = st.selectbox("분포 볼 컬럼(숫자형)", numeric_cols)
        if col1:
            fig, ax = plt.subplots()
            ax.hist(df[col1].dropna(), bins=20, color='deepskyblue', edgecolor='gray')
            ax.set_xlabel(col1)
            ax.set_ylabel("빈도")
            st.pyplot(fig)

    # 2. x/y 산점도
    if len(numeric_cols) >= 2:
        st.subheader("x/y 산점도 (숫자형만)")
        colx = st.selectbox("x축", numeric_cols, key="xscat")
        coly = st.selectbox("y축", numeric_cols, key="yscat")
        if colx and coly:
            fig2, ax2 = plt.subplots()
            ax2.scatter(df[colx], df[coly], alpha=0.5, color='orange')
            ax2.set_xlabel(colx)
            ax2.set_ylabel(coly)
            st.pyplot(fig2)

    # 3. 막대그래프 (카테고리형)
    if nonnum_cols and numeric_cols:
        st.subheader("카테고리별 평균/빈도 막대그래프")
        cat = st.selectbox("카테고리(문자/범주형)", nonnum_cols)
        val = st.selectbox("값(숫자형)", numeric_cols, key="barval")
        mode = st.radio("표시방식", ["평균값", "빈도수"])
        fig3, ax3 = plt.subplots()
        if mode == "평균값":
            df.groupby(cat)[val].mean().sort_values(ascending=False).plot(kind="bar", ax=ax3, color='teal')
            ax3.set_ylabel(f"{val} (평균)")
        else:
            df[cat].value_counts().plot(kind="bar", ax=ax3, color='salmon')
            ax3.set_ylabel("빈도수")
        st.pyplot(fig3)

    # 4. 연도별 변화 꺾은선 (연/월 컬럼 있을 때)
    year_candidates = [c for c in df.columns if "year" in c.lower() or "연도" in c]
    if year_candidates and numeric_cols:
        st.subheader("연도별 변화 (꺾은선)")
        ycol = st.selectbox("연도컬럼", year_candidates)
        vcol = st.selectbox("값(숫자)", numeric_cols, key="lineval")
        gr = df.groupby(ycol)[vcol].mean()
        fig4, ax4 = plt.subplots()
        gr.plot(ax=ax4, marker='o')
        ax4.set_ylabel(f"{vcol}(평균)")
        ax4.set_xlabel(ycol)
        st.pyplot(fig4)

    st.markdown("---")
    st.write("필요한 분석/그래프 추가 요청 OK! 파일이 안맞으면 미리보기 붙여주면 완전 맞춤으로 해줄 수 있음.")
else:
    st.info("csv/item/tsv/dat 파일을 업로드하면 자동 시각화 기능을 쓸 수 있습니다!")
