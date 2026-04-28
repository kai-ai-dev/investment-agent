import os
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = "./chroma_db"
REPORTS_DIR = "./reports"

def parse_pdf(pdf_path: str) -> str:
    """解析 PDF 提取文本"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def build_vectorstore(stock_code: str):
    """读取 reports/ 下所有 PDF，构建向量库"""
    # 1. 读取所有 PDF
    docs = []
    for filename in os.listdir(REPORTS_DIR):
        if filename.endswith(".pdf"):
            path = os.path.join(REPORTS_DIR, filename)
            print(f"正在解析：{filename}")
            text = parse_pdf(path)
            if text.strip():
                docs.append(text)
    
    if not docs:
        print("reports/ 目录下没有找到 PDF 文件")
        return None

    # 2. 切块
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "，", " "]
    )
    chunks = splitter.create_documents(
        docs,
        metadatas=[{"stock_code": stock_code, "source": f"report_{i}"}
                   for i in range(len(docs))]
    )
    print(f"共切出 {len(chunks)} 个文本块")

    # 3. Embedding + 存入 Chroma
    print("正在加载 embedding 模型（首次需要下载，约几分钟）...")
    embeddings = HuggingFaceEmbeddings(
        model_name="shibing624/text2vec-base-chinese"
    )
    vectorstore = Chroma.from_documents(
        chunks,
        embeddings,
        collection_name=f"stock_{stock_code}",
        persist_directory=CHROMA_DIR
    )
    print(f"向量库构建完成，共存入 {len(chunks)} 条记录")
    return vectorstore

def get_vectorstore(stock_code: str):
    """加载已有向量库"""
    embeddings = HuggingFaceEmbeddings(
        model_name="shibing624/text2vec-base-chinese"
    )
    return Chroma(
        collection_name=f"stock_{stock_code}",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )

def search_reports(query: str, stock_code: str, k: int = 4) -> str:
    """语义检索研报内容"""
    try:
        vectorstore = get_vectorstore(stock_code)
        docs = vectorstore.similarity_search(
            query, k=k,
            filter={"stock_code": stock_code}
        )
        if not docs:
            return "未找到相关研报内容"
        return "\n\n---\n\n".join([d.page_content for d in docs])
    except Exception as e:
        return f"研报检索失败：{e}"

if __name__ == "__main__":
    # 首次运行：构建向量库
    print("=== 构建向量库 ===")
    build_vectorstore("600519")

    # 测试检索
    print("\n=== 测试检索 ===")
    result = search_reports("茅台的营收增长情况", "600519")
    print(result[:500])