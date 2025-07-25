import streamlit as st
import pandas as pd

st.title("🗂️ 파일 확장자 상관없는 데이터 뷰어")
file = st.file_uploader("데이터 파일 업로드 (.csv, .tsv, .item 등)", type=["csv", "tsv", "item", "dat"])

if file:
    # 확장자 보고 기본 구분자 추천
    if file.name.endswith('.tsv'):
        sep = '\t'
    elif file.name.endswith('.item') or file.name.endswith('.dat'):
        sep = '|'
    else:
        sep = ','
    st.write(f"자동 감지된 구분자: `{sep}`")
    # 옵션: 직접 구분자 선택
    sep = st.text_input("구분자(예: , | \\t)", sep)
    try:
        df = pd.read_csv(file, sep=sep, encoding='latin1', nrows=50)
        st.dataframe(df)
        st.success(f"열(column) 목록: {list(df.columns)}")
    except Exception as e:
        st.error(f"불러오기 실패: {e}")

    # 만약 컬럼명이 없으면 직접 입력
    if st.checkbox("헤더 없음(첫줄이 데이터)"):
        cols = st.text_input("컬럼명 콤마로 입력", "col1,col2,col3")
        df = pd.read_csv(file, sep=sep, names=cols.split(','), encoding='latin1')
        st.dataframe(df)
