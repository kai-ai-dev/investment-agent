import os

import yfinance as yf

def get_stock_history(stock_code: str) -> str:
    """获取近30日日K行情，A股代码自动转换"""
    try:
        # A股代码转换：600519 -> 600519.SS，000858 -> 000858.SZ
        if stock_code.startswith("6"):
            ticker = f"{stock_code}.SS"
        else:
            ticker = f"{stock_code}.SZ"
        df = yf.download(ticker, period="1mo", progress=False)
        df.index = df.index.strftime("%Y-%m-%d")
        return df[["Open", "Close", "High", "Low", "Volume"]].tail(30).to_string()
    except Exception as e:
        return f"行情数据获取失败：{e}"

def get_stock_info(stock_code: str) -> str:
    """获取股票基本面信息"""
    try:
        if stock_code.startswith("6"):
            ticker = f"{stock_code}.SS"
        else:
            ticker = f"{stock_code}.SZ"
        info = yf.Ticker(ticker).info
        result = f"股票简称：{info.get('longName', '')}\n"
        result += f"行业：{info.get('industry', '')}\n"
        result += f"市值：{info.get('marketCap', '')}\n"
        result += f"市盈率PE：{info.get('trailingPE', '')}\n"
        result += f"52周最高：{info.get('fiftyTwoWeekHigh', '')}\n"
        result += f"52周最低：{info.get('fiftyTwoWeekLow', '')}"
        return result
    except Exception as e:
        return f"基本面数据获取失败：{e}"

def get_financial_metrics(stock_code: str) -> str:
    """获取财务指标"""
    try:
        if stock_code.startswith("6"):
            ticker = f"{stock_code}.SS"
        else:
            ticker = f"{stock_code}.SZ"
        info = yf.Ticker(ticker).info
        result = f"股票：{info.get('longName', '')}（{stock_code}）\n"
        result += f"最新价：{info.get('currentPrice', '')}\n"
        result += f"总市值：{info.get('marketCap', '')}\n"
        result += f"ROE：{info.get('returnOnEquity', '')}\n"
        result += f"毛利率：{info.get('grossMargins', '')}"
        return result
    except Exception as e:
        return f"财务指标获取失败：{e}"

if __name__ == "__main__":
    code = "600519"
    print("=== 近30日行情 ===")
    print(get_stock_history(code))
    print("\n=== 基本面信息 ===")
    print(get_stock_info(code))
    print("\n=== 财务指标 ===")
    print(get_financial_metrics(code))