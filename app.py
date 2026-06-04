import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='홈앤쇼핑 일일 매출 현황', layout='wide')

df = pd.read_csv('data/sales.csv')
df['date'] = pd.to_datetime(df['date'])

today = df['date'].max()
yesterday = today - pd.Timedelta(days=1)

today_sales = df[df['date'] == today]['sales'].sum()
yesterday_sales = df[df['date'] == yesterday]['sales'].sum()
change_amount = today_sales - yesterday_sales
change_pct = (change_amount / yesterday_sales * 100) if yesterday_sales > 0 else 0

st.markdown('# 홈앤쇼핑 일일 매출 현황')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        '오늘 매출',
        f'₩{today_sales:,}',
        delta=None,
    )

with col2:
    st.metric(
        '어제 매출',
        f'₩{yesterday_sales:,}',
        delta=None,
    )

with col3:
    st.metric(
        '어제 대비 증감률',
        f'{change_pct:+.1f}%',
        delta=f'₩{change_amount:+,}',
    )

st.divider()

daily_sales = df.groupby('date')['sales'].sum().reset_index()
daily_sales.columns = ['날짜', '매출']

line_chart = px.line(
    daily_sales,
    x='날짜',
    y='매출',
    title='일별 매출 추이',
    markers=True,
)

line_chart.update_traces(
    line=dict(color='#4e79a7', width=2),
    marker=dict(size=6),
    hovertemplate='<b>%{x|%Y-%m-%d}</b><br>₩%{y:,.0f}<extra></extra>',
)

line_chart.update_layout(
    xaxis_title='날짜',
    yaxis_title='매출',
    hovermode='x unified',
    plot_bgcolor='#f8f9fb',
    paper_bgcolor='#ffffff',
    font=dict(family='Malgun Gothic, AppleGothic, NanumGothic, sans-serif', size=13),
    yaxis=dict(
        tickformat=',.0f',
        tickprefix='₩',
    ),
)

category_sales = df.groupby('category')['sales'].sum().reset_index()
category_sales.columns = ['카테고리', '매출']

pie_chart = px.pie(
    category_sales,
    names='카테고리',
    values='매출',
    title='카테고리별 매출 비중',
    color_discrete_sequence=['#4e79a7', '#f28e2b', '#59a14f', '#e15759', '#76b7b2'],
)

pie_chart.update_traces(
    hovertemplate='<b>%{label}</b><br>₩%{value:,.0f}<br>%{percent}<extra></extra>',
)

pie_chart.update_layout(
    plot_bgcolor='#f8f9fb',
    paper_bgcolor='#ffffff',
    font=dict(family='Malgun Gothic, AppleGothic, NanumGothic, sans-serif', size=13),
)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.plotly_chart(line_chart, use_container_width=True)

with col_chart2:
    st.plotly_chart(pie_chart, use_container_width=True)
