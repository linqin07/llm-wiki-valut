# 13 - RAG 基础（Retrieval-Augmented Generation）

## 目录

1. [RAG 概念介绍](#1-rag-概念介绍)
2. [RAG 工作流程](#2-rag-工作流程)
3. [文档加载](#3-文档加载)
4. [文本分块](#4-文本分块)
5. [嵌入（Embedding）](#5-嵌入embedding)
6. [向量存储](#6-向量存储)
7. [相似度搜索](#7-相似度搜索)
8. [RAG 问答 Agent](#8-rag-问答-agent)
9. [已知问题](#9-已知问题)
10. [完整代码示例](#10-完整代码示例)
11. [常见错误](#11-常见错误)
12. [最佳实践](#12-最佳实践)
13. [练习题](#13-练习题)

---

## 1. RAG 概念介绍

### 什么是 RAG

RAG（Retrieval-Augmented Generation，检索增强生成）是一种让 AI 基于你的数据回答问题的技术。

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG 的核心思想                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  传统LLM:                                                   │
│  用户问题 → LLM → 回答（基于训练数据，可能过时或不准确）       │
│                                                             │
│  RAG:                                                       │
│  用户问题 → 检索相关文档 → LLM + 文档 → 回答（基于你的数据）  │
│                                                             │
│  优势:                                                      │
│  1. 基于最新数据回答                                         │
│  2. 减少幻觉（Hallucination）                               │
│  3. 可以引用来源                                             │
│  4. 无需微调模型                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### RAG 的应用场景

| 场景 | 描述 | 示例 |
|------|------|------|
| 企业知识库 | 基于内部文档回答问题 | 公司政策、产品文档 |
| 客户支持 | 基于FAQ回答客户问题 | 退货政策、使用说明 |
| 学术研究 | 基于论文回答问题 | 文献综述、技术细节 |
| 法律咨询 | 基于法规回答问题 | 合同条款、法律规定 |
| 个人助手 | 基于个人笔记回答问题 | 日记、笔记、收藏 |

---

## 2. RAG 工作流程

### 完整流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG 完整工作流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  离线阶段（索引构建）:                                        │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ 文档     │───→│ 分块     │───→│ 嵌入     │              │
│  │ 加载     │    │ Split    │    │ Embed    │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                       │                     │
│                                       ▼                     │
│                               ┌──────────┐                 │
│                               │ 向量存储 │                 │
│                               │ VectorDB │                 │
│                               └──────────┘                 │
│                                                             │
│  在线阶段（查询应答）:                                        │
│                                                             │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ 用户     │───→│ 相似度   │───→│ 检索     │              │
│  │ 查询     │    │ 搜索     │    │ Top-K    │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                       │                     │
│                                       ▼                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ 回答     │←───│ LLM      │←───│ 组合     │              │
│  │ 生成     │    │ 生成     │    │ Prompt   │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 详细步骤说明

```
步骤1: 文档加载
┌─────────────────────────────────────────────────────────┐
│ 输入: 文档文件（PDF, TXT, DOCX, HTML, ...）              │
│ 输出: 文档对象列表                                       │
│ 工具: TextLoader, PDFLoader, ...                        │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
步骤2: 文本分块
┌─────────────────────────────────────────────────────────┐
│ 输入: 文档对象列表                                       │
│ 输出: 文本块列表（每个块500-2000字符）                    │
│ 工具: RecursiveCharacterTextSplitter                    │
│ 参数: chunk_size=1000, chunk_overlap=200                │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
步骤3: 生成嵌入
┌─────────────────────────────────────────────────────────┐
│ 输入: 文本块列表                                         │
│ 输出: 向量列表（每个向量384/768/1536维）                  │
│ 工具: HuggingFaceEmbeddings, OpenAIEmbeddings           │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
步骤4: 存储向量
┌─────────────────────────────────────────────────────────┐
│ 输入: 文本块 + 向量                                      │
│ 输出: 向量数据库                                         │
│ 工具: Pinecone, Chroma, FAISS, ...                      │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 文档加载

### TextLoader 加载文本文件

```python
from langchain_community.document_loaders import TextLoader

# 加载文本文件
loader = TextLoader("path/to/document.txt", encoding="utf-8")
documents = loader.load()

# documents 是一个列表，每个元素是一个Document对象
print(f"加载了 {len(documents)} 个文档")
print(f"第一个文档的内容: {documents[0].page_content[:100]}...")
print(f"元数据: {documents[0].metadata}")
```

### 多种文档格式

```python
# 文本文件
from langchain_community.document_loaders import TextLoader

# PDF文件
from langchain_community.document_loaders import PyPDFLoader

# CSV文件
from langchain_community.document_loaders import CSVLoader

# HTML文件
from langchain_community.document_loaders import BSHTMLLoader

# Word文件
from langchain_community.document_loaders import Docx2txtLoader

# Markdown文件
from langchain_community.document_loaders import UnstructuredMarkdownLoader
```

### 代码示例：加载多种格式

```python
"""
文档加载示例
"""
from langchain_community.document_loaders import TextLoader, PyPDFLoader
import os


def load_documents(directory: str):
    """加载目录中的所有文档"""

    documents = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        if filename.endswith(".txt"):
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())
            print(f"加载文本文件: {filename}")

        elif filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())
            print(f"加载PDF文件: {filename}")

    print(f"\n总共加载了 {len(documents)} 个文档")
    return documents


if __name__ == "__main__":
    docs = load_documents("data/documents")
    for doc in docs[:3]:
        print(f"内容预览: {doc.page_content[:100]}...")
```

---

## 4. 文本分块

### RecursiveCharacterTextSplitter

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 创建文本分割器
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # 每个块的最大字符数
    chunk_overlap=200,    # 块之间的重叠字符数
    length_function=len,  # 计算长度的函数
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]  # 分隔符优先级
)

# 分割文档
chunks = splitter.split_documents(documents)

print(f"原始文档数: {len(documents)}")
print(f"分割后块数: {len(chunks)}")
```

### chunk_size 和 chunk_overlap 参数

```
┌─────────────────────────────────────────────────────────────┐
│              chunk_size 和 chunk_overlap 原理                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  原始文本: "这是一段很长的文本，需要被分割成多个块..."         │
│                                                             │
│  chunk_size = 100, chunk_overlap = 20:                      │
│                                                             │
│  块1: "这是一段很长的文本，需要被分割" [0-100]               │
│  块2: "要被分割成多个块..." [80-180]                         │
│        ↑                                                    │
│        └── 重叠部分（20字符）                                │
│                                                             │
│  重叠的作用:                                                 │
│  - 保持上下文连续性                                          │
│  - 避免重要信息被截断                                        │
│  - 提高检索准确性                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 分块策略选择

```python
"""
不同分块策略示例
"""
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
)


def strategy_examples():
    """分块策略示例"""

    text = "这是一段很长的文本..." * 100

    # 策略1: 按字符数分割（推荐）
    splitter1 = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
    )

    # 策略2: 按固定字符分割
    splitter2 = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separator="\n"
    )

    # 策略3: 按Token数分割
    splitter3 = TokenTextSplitter(
        chunk_size=500,    # 500 tokens
        chunk_overlap=50   # 50 tokens overlap
    )

    # 应用不同策略
    chunks1 = splitter1.split_text(text)
    chunks2 = splitter2.split_text(text)
    chunks3 = splitter3.split_text(text)

    print(f"策略1（递归字符）: {len(chunks1)} 块")
    print(f"策略2（固定字符）: {len(chunks2)} 块")
    print(f"策略3（Token）: {len(chunks3)} 块")


if __name__ == "__main__":
    strategy_examples()
```

### 分块大小建议

| 场景 | chunk_size | chunk_overlap | 说明 |
|------|-----------|---------------|------|
| 短文档 | 500 | 100 | 快速检索 |
| 长文档 | 1000 | 200 | 平衡检索和上下文 |
| 技术文档 | 1500 | 300 | 保留更多上下文 |
| 对话记录 | 2000 | 400 | 保留完整对话 |

---

## 5. 嵌入（Embedding）

### HuggingFace 嵌入模型

```python
from langchain_huggingface import HuggingFaceEmbeddings

# 使用HuggingFace的all-MiniLM-L6-v2模型
# 384维向量，适合英文和中文
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},  # 使用CPU，或"cuda"使用GPU
    encode_kwargs={"normalize_embeddings": True}  # 归一化向量
)

# 生成嵌入向量
text = "这是一个测试文本"
vector = embeddings.embed_query(text)

print(f"文本: {text}")
print(f"向量维度: {len(vector)}")  # 384
print(f"向量前5个值: {vector[:5]}")
```

### 嵌入的概念

```
┌─────────────────────────────────────────────────────────────┐
│              嵌入（Embedding）概念                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  文本: "猫是一种可爱的动物"                                   │
│                                                             │
│  嵌入模型将文本转换为向量:                                    │
│  [0.12, -0.34, 0.56, ..., 0.78]  (384维)                   │
│                                                             │
│  向量的特性:                                                 │
│  - 语义相似的文本，向量距离近                                 │
│  - 语义不同的文本，向量距离远                                 │
│                                                             │
│  示例:                                                      │
│  "猫是可爱的动物" → [0.12, -0.34, ...]                      │
│  "小猫很萌"       → [0.11, -0.33, ...]  (距离近)            │
│  "今天天气很好"   → [0.89, 0.23, ...]   (距离远)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 常用嵌入模型

| 模型 | 维度 | 特点 | 适用场景 |
|------|------|------|---------|
| all-MiniLM-L6-v2 | 384 | 轻量级，速度快 | 通用场景 |
| all-mpnet-base-v2 | 768 | 精度高 | 需要高精度 |
| text-embedding-ada-002 | 1536 | OpenAI模型 | 英文为主 |
| text-embedding-3-small | 1536 | OpenAI最新 | 多语言 |

---

## 6. 向量存储

### Pinecone 向量存储

```python
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os

# 初始化Pinecone
os.environ["PINECONE_API_KEY"] = "your-api-key"

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# 创建索引（如果不存在）
index_name = "my-knowledge-base"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  # 与嵌入模型维度一致
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# 创建向量存储
vectorstore = PineconeVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=index_name
)

print(f"已将 {len(chunks)} 个文本块存储到Pinecone")
```

### 存储和索引嵌入向量

```python
"""
向量存储详细示例
"""
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document


def create_vectorstore(chunks: list, index_name: str):
    """创建向量存储"""

    # 初始化嵌入模型
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # 创建向量存储
    vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=index_name
    )

    return vectorstore


def add_documents(vectorstore, new_docs: list):
    """添加新文档到向量存储"""
    vectorstore.add_documents(new_docs)
    print(f"添加了 {len(new_docs)} 个文档")
```

---

## 7. 相似度搜索

### 基本相似度搜索

```python
"""
相似度搜索示例
"""
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore


def similarity_search_example():
    """相似度搜索示例"""

    # 初始化嵌入模型
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # 连接到已有的向量存储
    vectorstore = PineconeVectorStore(
        index_name="my-knowledge-base",
        embedding=embeddings
    )

    # 执行相似度搜索
    query = "Python装饰器怎么用？"
    results = vectorstore.similarity_search(
        query=query,
        k=3  # 返回最相似的3个结果
    )

    print(f"查询: {query}")
    print(f"找到 {len(results)} 个相关文档：\n")

    for i, doc in enumerate(results, 1):
        print(f"结果 {i}:")
        print(f"  内容: {doc.page_content[:200]}...")
        print(f"  来源: {doc.metadata.get('source', '未知')}")
        print()


if __name__ == "__main__":
    similarity_search_example()
```

### 带分数的搜索

```python
def similarity_search_with_score():
    """带分数的相似度搜索"""

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = PineconeVectorStore(
        index_name="my-knowledge-base",
        embedding=embeddings
    )

    query = "什么是机器学习？"

    # 带分数的搜索
    results = vectorstore.similarity_search_with_score(
        query=query,
        k=3
    )

    print(f"查询: {query}\n")

    for doc, score in results:
        print(f"相似度分数: {score:.4f}")
        print(f"内容: {doc.page_content[:200]}...")
        print()
```

---

## 8. RAG 问答 Agent

### 自定义 search_kb 工具

```python
"""
RAG问答Agent示例
"""
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langgraph.checkpoint.memory import InMemorySaver


# 全局向量存储（在实际应用中应该单独管理）
_vectorstore = None


def get_vectorstore():
    """获取向量存储实例"""
    global _vectorstore
    if _vectorstore is None:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        _vectorstore = PineconeVectorStore(
            index_name="my-knowledge-base",
            embedding=embeddings
        )
    return _vectorstore


@tool
def search_knowledge_base(query: str) -> str:
    """
    搜索知识库，查找与查询相关的文档。

    参数:
        query: 搜索查询，描述你要查找的信息

    返回:
        相关文档的内容摘要
    """
    vectorstore = get_vectorstore()

    # 执行相似度搜索
    results = vectorstore.similarity_search(query, k=3)

    if not results:
        return "未找到相关文档"

    # 格式化结果
    formatted_results = []
    for i, doc in enumerate(results, 1):
        content = doc.page_content[:500]  # 限制长度
        source = doc.metadata.get("source", "未知来源")
        formatted_results.append(f"文档{i} (来源: {source}):\n{content}")

    return "\n\n".join(formatted_results)


def create_rag_agent():
    """创建RAG问答Agent"""

    model = init_chat_model("groq:llama-3.3-70b-versatile")
    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model,
        tools=[search_knowledge_base],
        system_prompt="""你是一个知识库问答助手。

当用户提出问题时：
1. 使用search_knowledge_base工具搜索相关文档
2. 基于搜索结果回答问题
3. 引用来源信息
4. 如果没有找到相关信息，如实告知用户

回答要求：
- 准确引用文档内容
- 不要编造信息
- 保持回答简洁明了""",
        checkpointer=checkpointer
    )

    return agent


def rag_qa_example():
    """RAG问答示例"""

    agent = create_rag_agent()
    config = {"configurable": {"thread_id": "rag-demo"}}

    # 模拟问答
    questions = [
        "什么是Python装饰器？",
        "如何使用Python的上下文管理器？",
        "Python的GIL是什么？",
    ]

    for question in questions:
        print(f"\n问题: {question}")
        response = agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            config=config
        )
        print(f"回答: {response['messages'][-1].content}")


if __name__ == "__main__":
    rag_qa_example()
```

---

## 9. 已知问题

### Groq tool calls 中 Unicode 参数的成功率

```
┌─────────────────────────────────────────────────────────────┐
│              已知问题：Unicode参数成功率                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  问题描述:                                                   │
│  在使用Groq模型时，tool_calls中的Unicode参数（如中文）        │
│  成功率约为70-80%，可能返回乱码或截断。                       │
│                                                             │
│  示例:                                                      │
│  预期: search_knowledge_base(query="Python装饰器怎么用")     │
│  实际: search_knowledge_base(query="Python")                │
│                                                             │
│  解决方案:                                                   │
│  1. 使用英文查询关键词                                       │
│  2. 在工具内部处理中文查询                                   │
│  3. 使用备用模型（如OpenAI）                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 解决方案示例

```python
@tool
def search_knowledge_base(query: str) -> str:
    """搜索知识库"""

    # 处理可能的Unicode问题
    if len(query) < 3:
        # 可能是Unicode截断，尝试从上下文获取完整查询
        return "请提供更详细的查询关键词"

    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=3)

    if not results:
        return "未找到相关文档"

    return "\n\n".join([doc.page_content[:500] for doc in results])
```

---

## 10. 完整代码示例

### 示例1：完整的 RAG 系统

```python
"""
完整的RAG系统示例
"""
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from pinecone import Pinecone, ServerlessSpec


class RAGSystem:
    """RAG系统"""

    def __init__(self, index_name: str = "knowledge-base"):
        self.index_name = index_name
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        self.vectorstore = None
        self.agent = None

    def initialize_pinecone(self):
        """初始化Pinecone"""
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

        if self.index_name not in pc.list_indexes().names():
            pc.create_index(
                name=self.index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )

        self.vectorstore = PineconeVectorStore(
            index_name=self.index_name,
            embedding=self.embeddings
        )

    def load_documents(self, directory: str):
        """加载文档"""
        documents = []

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)

            if filename.endswith(".txt"):
                loader = TextLoader(filepath, encoding="utf-8")
                documents.extend(loader.load())
                print(f"加载: {filename}")

        # 分块
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
        )
        chunks = splitter.split_documents(documents)
        print(f"分块完成: {len(chunks)} 个块")

        # 存储到向量数据库
        self.vectorstore.add_documents(chunks)
        print(f"已存储到Pinecone")

    def create_agent(self):
        """创建RAG Agent"""

        @tool
        def search_kb(query: str) -> str:
            """搜索知识库"""
            results = self.vectorstore.similarity_search(query, k=3)
            if not results:
                return "未找到相关文档"
            return "\n\n".join([doc.page_content[:500] for doc in results])

        model = init_chat_model("groq:llama-3.3-70b-versatile")
        checkpointer = InMemorySaver()

        self.agent = create_agent(
            model=model,
            tools=[search_kb],
            system_prompt="你是知识库助手。使用search_kb工具搜索信息，基于搜索结果回答问题。",
            checkpointer=checkpointer
        )

    def ask(self, question: str, thread_id: str = "default") -> str:
        """提问"""
        config = {"configurable": {"thread_id": thread_id}}
        response = self.agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            config=config
        )
        return response["messages"][-1].content


def main():
    """主函数"""
    rag = RAGSystem()

    # 初始化
    rag.initialize_pinecone()

    # 加载文档
    rag.load_documents("data/documents")

    # 创建Agent
    rag.create_agent()

    # 问答
    while True:
        question = input("\n请输入问题（输入'quit'退出）: ")
        if question.lower() == "quit":
            break

        answer = rag.ask(question)
        print(f"\n回答: {answer}")


if __name__ == "__main__":
    main()
```

---

## 11. 常见错误

### 错误1：chunk_size 设置不当

```python
# 错误：chunk_size太小
splitter = RecursiveCharacterTextSplitter(chunk_size=100)
# 问题：块太小，丢失上下文

# 错误：chunk_size太大
splitter = RecursiveCharacterTextSplitter(chunk_size=10000)
# 问题：块太大，检索不精确

# 正确：根据场景选择合适的大小
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
```

### 错误2：嵌入维度不匹配

```python
# 错误：Pinecone索引维度与嵌入模型维度不一致
pc.create_index(name="test", dimension=768)  # 768维
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # 384维
# 问题：维度不匹配，无法存储

# 正确：确保维度一致
pc.create_index(name="test", dimension=384)  # 384维
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # 384维
```

### 错误3：未处理空结果

```python
# 错误：未处理搜索结果为空的情况
results = vectorstore.similarity_search(query, k=3)
return results[0].page_content  # 可能IndexError

# 正确：检查结果是否为空
results = vectorstore.similarity_search(query, k=3)
if not results:
    return "未找到相关文档"
return results[0].page_content
```

### 错误4：未设置Pinecone API Key

```python
# 错误：未设置环境变量
os.environ["PINECONE_API_KEY"] = ""  # 空值

# 正确：设置有效的API Key
os.environ["PINECONE_API_KEY"] = "your-actual-api-key"
```

---

## 12. 最佳实践

### 1. 选择合适的分块策略

```python
# 根据文档类型选择分块策略
if doc_type == "技术文档":
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300
    )
elif doc_type == "对话记录":
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=400
    )
else:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
```

### 2. 使用元数据过滤

```python
# 在搜索时使用元数据过滤
results = vectorstore.similarity_search(
    query="Python装饰器",
    k=3,
    filter={"source": "python_tutorial.txt"}  # 只搜索特定来源
)
```

### 3. 定期更新索引

```python
def update_index(vectorstore, new_docs_dir: str):
    """定期更新索引"""
    new_docs = load_documents(new_docs_dir)
    new_chunks = splitter.split_documents(new_docs)
    vectorstore.add_documents(new_chunks)
    print(f"更新了 {len(new_chunks)} 个文档块")
```

### 4. 监控搜索质量

```python
def evaluate_search_quality(vectorstore, test_queries: list):
    """评估搜索质量"""
    for query, expected_keywords in test_queries:
        results = vectorstore.similarity_search(query, k=3)
        found = any(
            keyword in doc.page_content
            for doc in results
            for keyword in expected_keywords
        )
        status = "✓" if found else "✗"
        print(f"{status} {query}")
```

---

## 13. 练习题

### 练习1：基础 RAG

实现一个简单的 RAG 系统：
1. 加载一个文本文件
2. 分块并存储到向量数据库
3. 实现基本的问答功能

### 练习2：多文档 RAG

扩展 RAG 系统支持多文档：
1. 加载多个不同格式的文件（TXT, PDF）
2. 使用元数据标记来源
3. 实现按来源过滤搜索

### 练习3：RAG Agent

创建一个 RAG Agent：
1. 实现 search_kb 工具
2. 支持多轮对话
3. 能够引用来源信息

### 练习4：搜索优化

优化 RAG 系统的搜索质量：
1. 尝试不同的 chunk_size 和 chunk_overlap
2. 比较不同嵌入模型的效果
3. 实现带分数的搜索，设置相似度阈值

---

[上一章：12-验证与重试](./12-验证与重试.md) | [返回目录](#目录) | [下一章：14-RAG进阶](./14-RAG进阶.md)
