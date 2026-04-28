# 📊 AI 投研助手 Agent

> 基于 LangGraph ReAct Agent + RAG 的 A 股智能投研分析工具

🔗 **[在线 Demo](https://investment-agent-evj4or4qcmmpcblodhhupd.streamlit.app)**

## 项目简介

输入 A 股股票代码，Agent 自动调度多个工具，生成包含基本面、研报观点、风险提示的结构化投研报告。

## 技术架构

| 层级 | 技术选型 |
|------|---------|
| Agent 编排 | LangGraph（ReAct 模式）|
| LLM | DeepSeek Chat |
| 数据接入 | yfinance（行情/财务）|
| RAG | text2vec-base-chinese + Chroma 向量库 |
| 前端 | Streamlit + Plotly |
| 部署 | Streamlit Cloud |

## 核心功能

- **行情数据**：近30日 K 线 + PE/ROE/毛利率等财务指标
- **研报检索**：基于语义相似度召回年报/研报关键段落（RAG）
- **Agent 编排**：ReAct 模式自主决定工具调用顺序
- **结构化报告**：基本面 → 研报观点 → 风险提示 → 综合建议
- **对话追问**：报告生成后支持多轮追问

## 快速开始

```bash
git clone https://github.com/kai-ai-dev/investment-agent.git
cd investment-agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 支持股票

| 代码 | 名称 |
|------|------|
| 600519 | 贵州茅台 |
| 000858 | 五粮液 |
| 300750 | 宁德时代 |

## 简历描述

> 基于 LangGraph ReAct 模式构建 A 股投研 Agent，集成 yfinance 行情接口与 RAG 研报检索（Chroma + text2vec-base-chinese），实现多工具自主编排、结构化投研报告生成。前端采用 Streamlit + Plotly，部署至 Streamlit Cloud。核心技术：LLM Tool Use、RAG、向量数据库、Agentic Loop。