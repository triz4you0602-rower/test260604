import os

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='홈앤쇼핑 일일 매출 현황', layout='wide')

def load_sales_data():
    try:
        from supabase import create_client, Client
        url = st.secrets.get("supabase", {}).get("url")
        key = st.secrets.get("supabase", {}).get("key")
        if url and key:
            supabase = create_client(url, key)
            response = supabase.table('sales').select('*').execute()
            df = pd.DataFrame(response.data)
            df['date'] = pd.to_datetime(df['date'])
            return df
    except Exception as e:
        st.warning(f"Supabase 연결 실패: {e}. CSV 파일을 사용합니다.")

    df = pd.read_csv('data/sales.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_sales_data()

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

st.divider()

st.markdown('## 오늘 매출 AI 요약')


def get_anthropic_api_key():
    # secrets.toml이 없으면 st.secrets 접근 자체가 예외를 던지므로 감싼다
    try:
        key = st.secrets.get("anthropic", {}).get("api_key")
        if key:
            return key
        key = st.secrets.get("ANTHROPIC_API_KEY")
        if key:
            return key
    except Exception:
        pass
    return os.environ.get("ANTHROPIC_API_KEY")


def build_sales_brief(df, target_date):
    day_df = df[df['date'].dt.date == target_date]
    prev_date = target_date - pd.Timedelta(days=1)
    prev_df = df[df['date'].dt.date == prev_date]

    total_sales = day_df['sales'].sum()
    total_orders = day_df['orders'].sum()
    prev_sales = prev_df['sales'].sum()
    change_pct = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0

    category_lines = [
        f"- {row['category']}: ₩{row['sales']:,} ({row['orders']}건)"
        for _, row in day_df.groupby('category')[['sales', 'orders']].sum().reset_index().iterrows()
    ]
    top_products = day_df.nlargest(5, 'sales')
    product_lines = [
        f"- {row['product']} ({row['category']}, {row['broadcast_time']}, 진행: {row['host']}): ₩{row['sales']:,} / {row['orders']}건"
        for _, row in top_products.iterrows()
    ]

    return f"""기준일: {target_date}
총 매출: ₩{total_sales:,} (전일 대비 {change_pct:+.1f}%)
총 주문: {total_orders:,}건
전일({prev_date}) 매출: ₩{prev_sales:,}

[카테고리별 매출]
{chr(10).join(category_lines)}

[매출 상위 5개 방송]
{chr(10).join(product_lines)}"""


available_dates = sorted(df['date'].dt.date.unique(), reverse=True)

col_date, col_btn = st.columns([2, 1])
with col_date:
    selected_date = st.selectbox(
        '기준일 선택',
        available_dates,
        format_func=lambda d: d.strftime('%Y-%m-%d'),
    )
with col_btn:
    st.write('')  # 버튼을 selectbox와 수직 정렬
    run_summary = st.button('오늘 매출 AI 요약', type='primary', use_container_width=True)

if run_summary:
    api_key = get_anthropic_api_key()
    if not api_key:
        st.info(
            "AI 요약을 사용하려면 Anthropic API 키가 필요합니다.\n\n"
            "다음 중 한 가지 방법으로 키를 설정해 주세요:\n"
            "1. `.streamlit/secrets.toml` 파일에 추가:\n"
            "```toml\n[anthropic]\napi_key = \"sk-ant-...\"\n```\n"
            "2. 또는 환경변수 `ANTHROPIC_API_KEY` 설정\n\n"
            "키는 https://console.anthropic.com 에서 발급할 수 있습니다."
        )
    else:
        import anthropic

        brief = build_sales_brief(df, selected_date)
        client = anthropic.Anthropic(api_key=api_key)

        def stream_summary():
            with client.messages.stream(
                model="claude-opus-4-8",
                max_tokens=2048,
                system=(
                    "당신은 홈쇼핑 회사의 매출 분석가입니다. "
                    "경영진에게 보고할 일일 매출 요약을 한국어로 작성합니다. "
                    "핵심 수치와 전일 대비 변화를 먼저 제시하고, 카테고리·방송별 특이사항과 "
                    "간단한 시사점을 덧붙이세요. 금액은 ₩ 기호와 천 단위 콤마로 표기하고, "
                    "마크다운 형식으로 간결하게 작성하세요."
                ),
                messages=[{"role": "user", "content": f"다음 매출 데이터를 요약해 주세요.\n\n{brief}"}],
            ) as stream:
                yield from stream.text_stream

        try:
            with st.spinner('AI 요약 생성 중...'):
                st.write_stream(stream_summary())
        except anthropic.AuthenticationError:
            st.error("API 키가 유효하지 않습니다. 키를 확인해 주세요.")
        except anthropic.RateLimitError:
            st.error("요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요.")
        except anthropic.APIConnectionError:
            st.error("네트워크 연결에 실패했습니다. 인터넷 연결을 확인해 주세요.")
        except anthropic.APIStatusError as e:
            st.error(f"API 오류가 발생했습니다 (status {e.status_code}). 잠시 후 다시 시도해 주세요.")
