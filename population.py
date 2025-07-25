import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("인구 피라미드 대시보드 (남/여/전체 연령구조)")

남여 = st.file_uploader("남여구분.csv 업로드", type="csv")
합계 = st.file_uploader("계.csv 업로드", type="csv")

if 남여 and 합계:
    df_mf = pd.read_csv(남여)
    df_sum = pd.read_csv(합계)

    # 예시: 컬럼 자동 감지 (구/시군구, 연령대, 남자, 여자/계)
    # (실제 파일 구조에 따라 아래 col 변수만 조정하면 됨)
    region_col = [c for c in df_mf.columns if '구' in c or '군' in c or '시' in c][0]
    age_col = [c for c in df_mf.columns if '세' in c or '연령' in c][0]
    male_col = [c for c in df_mf.columns if '남' in c][0]
    female_col = [c for c in df_mf.columns if '여' in c][0]

    # 시군구/구 선택
    regions = df_mf[region_col].unique()
    selected_region = st.selectbox("지역 선택", regions)
    dff = df_mf[df_mf[region_col]==selected_region]

    # 연령대(정렬)
    dff = dff.sort_values(by=age_col)
    ages = dff[age_col].tolist()
    male = dff[male_col].tolist()
    female = dff[female_col].tolist()

    # Plotly 피라미드 (남성 - 왼쪽/음수, 여성 - 오른쪽/양수)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=ages,
        x=[-x for x in male],  # 좌측(음수)로
        name='남자',
        orientation='h',
        marker_color='royalblue'
    ))
    fig.add_trace(go.Bar(
        y=ages,
        x=female,  # 우측(양수)로
        name='여자',
        orientation='h',
        marker_color='lightblue'
    ))
    fig.update_layout(
        barmode='relative',
        title=f"{selected_region} 연령대 인구 피라미드",
        xaxis=dict(title='인구수', tickvals=[-max(male), 0, max(female)],
                   ticktext=[f"{max(male):,}", "0", f"{max(female):,}"]),
        yaxis=dict(title='연령대'),
        bargap=0.2,
        plot_bgcolor='#fafbfc'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("남여구분.csv와 계.csv 파일을 모두 업로드하세요.")
