import os
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from agent import analyze_stock

st.set_page_config(
    page_title="投研助手 Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI 投研助手")
st.caption("基于 LangGraph ReAct Agent + RAG 研报检索")

# ── 侧边栏 ──
with st.sidebar:
    st.header("分析设置")
    stock_code = st.text_input(
        "股票代码",
        value="600519",
        placeholder="如 600519（茅台）"
    )
    st.caption("支持 A 股代码，如 600519、000858、300750")
    run = st.button("开始分析", type="primary", use_container_width=True)
    st.divider()
    st.markdown("**支持股票示例**")
    st.markdown("- 600519 贵州茅台")
    st.markdown("- 000858 五粮液")
    st.markdown("- 300750 宁德时代")

# ── 主区域 ──
if run and stock_code:
    # 转换 ticker
    ticker_code = f"{stock_code}.SS" if stock_code.startswith("6") else f"{stock_code}.SZ"

    # 指标卡
    with st.spinner("获取行情数据..."):
        try:
            ticker = yf.Ticker(ticker_code)
            info = ticker.info
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("最新价", f"¥{info.get('currentPrice', '--')}")
            col2.metric("市盈率 PE", round(info.get('trailingPE', 0), 2))
            col3.metric("ROE", f"{round(info.get('returnOnEquity', 0) * 100, 1)}%")
            col4.metric("毛利率", f"{round(info.get('grossMargins', 0) * 100, 1)}%")
        except:
            st.warning("行情指标获取失败，继续分析...")

    # K 线图
    with st.spinner("绘制走势图..."):
        try:
            hist = yf.download(ticker_code, period="1mo", progress=False)
            fig = go.Figure(go.Scatter(
                x=hist.index,
                y=hist["Close"].squeeze(),
                mode="lines",
                line=dict(color="#534AB7", width=2),
                fill="tozeroy",
                fillcolor="rgba(83,74,183,0.08)"
            ))
            fig.update_layout(
                title="近30日收盘价走势",
                margin=dict(l=0, r=0, t=40, b=0),
                height=250,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)")
            )
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.warning("走势图绘制失败，继续分析...")

    # Agent 分析
    st.subheader("🤖 AI 投研报告")
    query = f"请分析股票 {stock_code}，包括估值、研报观点和风险提示"

    with st.expander("查看 Agent 思考过程", expanded=False):
        st.info("Agent 正在调用工具：行情数据 → 财务指标 → 研报检索 → 综合报告")

    with st.spinner("Agent 分析中，请稍候（约30秒）..."):
        result = analyze_stock(query)

    st.markdown(result)
    st.divider()

    # 对话追问
    st.subheader("💬 继续追问")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("例如：和五粮液对比估值如何？"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("分析中..."):
                response = analyze_stock(f"关于股票{stock_code}：{prompt}")
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.info("👈 在左侧输入股票代码，点击「开始分析」")