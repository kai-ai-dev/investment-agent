import os

from langchain_core.tools import tool
from data import get_stock_history, get_stock_info, get_financial_metrics
from rag import search_reports

@tool
def tool_get_market_data(stock_code: str) -> str:
    """
    获取A股股票的近30日行情数据（开盘价、收盘价、最高价、最低价、成交量）。
    适合回答：股价走势、近期涨跌、交易量变化等问题。
    输入股票代码，如 600519（茅台）、000858（五粮液）。
    """
    history = get_stock_history(stock_code)
    info = get_stock_info(stock_code)
    return f"【近30日行情】\n{history}\n\n【基本面信息】\n{info}"

@tool
def tool_get_financial_metrics(stock_code: str) -> str:
    """
    获取股票的核心财务指标：市值、PE市盈率、ROE净资产收益率、毛利率等。
    适合回答：估值是否合理、盈利能力如何、和行业对比等问题。
    输入股票代码，如 600519（茅台）、000858（五粮液）。
    """
    return get_financial_metrics(stock_code)

@tool
def tool_search_reports(query: str, stock_code: str) -> str:
    """
    在研报和年报向量库中语义检索相关内容。
    适合回答：公司战略、竞争优势、风险因素、业务模式、分析师观点等问题。
    query 是检索关键词，stock_code 是股票代码。
    """
    return search_reports(query, stock_code)

if __name__ == "__main__":
    print("=== 测试 tool_get_market_data ===")
    print(tool_get_market_data.invoke({"stock_code": "600519"}))

    print("\n=== 测试 tool_get_financial_metrics ===")
    print(tool_get_financial_metrics.invoke({"stock_code": "600519"}))

    print("\n=== 测试 tool_search_reports ===")
    print(tool_search_reports.invoke({
        "query": "茅台的竞争优势",
        "stock_code": "600519"
    }))