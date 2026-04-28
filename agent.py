import os
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

import streamlit as st
if "DEEPSEEK_API_KEY" in st.secrets:
    os.environ["DEEPSEEK_API_KEY"] = st.secrets["DEEPSEEK_API_KEY"]

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools import tool_get_market_data, tool_get_financial_metrics, tool_search_reports

# DeepSeek 兼容 OpenAI 格式
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0
)

system_prompt = """你是一位专业的A股投研助手。

当用户询问某只股票时，请按以下步骤分析：
1. 用 tool_get_market_data 获取近期行情和基本面
2. 用 tool_get_financial_metrics 获取财务指标
3. 用 tool_search_reports 检索相关研报内容
4. 综合以上信息，输出结构化投研报告

报告格式：
## 基本面概览
（市值、PE、ROE、毛利率）

## 近期股价走势
（近期价格趋势描述）

## 研报核心观点
（从研报检索结果中提炼）

## 风险提示
（结合研报和财务数据）

## 综合建议
（仅供参考，非投资建议）
"""

tools = [tool_get_market_data, tool_get_financial_metrics, tool_search_reports]
agent = create_react_agent(llm, tools, prompt=system_prompt)

def analyze_stock(user_query: str) -> str:
    result = agent.invoke({
        "messages": [{"role": "user", "content": user_query}]
    })
    return result["messages"][-1].content

if __name__ == "__main__":
    print("=== Agent 分析茅台 ===")
    result = analyze_stock("帮我分析一下贵州茅台600519，重点看估值和研报观点")
    print(result)