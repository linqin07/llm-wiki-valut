# 14 - RAG 进阶（Advanced RAG）

## 目录

1. [向量搜索的局限性](#1-向量搜索的局限性)
2. [BM25 关键词搜索](#2-bm25-关键词搜索)
3. [混合搜索（Hybrid Search）](#3-混合搜索hybrid-search)
4. [倒数排名融合（RRF）](#4-倒数排名融合rrf)
5. [Chroma 向量存储](#5-chroma-向量存储)
6. [混合搜索优化策略](#6-混合搜索优化策略)
7. [完整代码示例](#7-完整代码示例)
8. [常见错误](#8-常见错误)
9. [最佳实践](#9-最佳实践)
10. [练习题](#10-练习题)

---

## 1. 向量搜索的局限性

### 语义理解好，但关键词匹配弱

```
┌─────────────────────────────────────────────────────────────┐
│              向量搜索的局限性                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  优势（语义理解）:                                            │
│  - "如何学习Python" 能匹配到 "Python入门教程"                 │
│  - "机器学习算法" 能匹配到 "ML模型训练方法"                   │
│  - 理解同义词和近义词                                         │
│                                                             │
│  劣势（关键词匹配）:                                          │
│  - "error 404" 可能匹配不到 "HTTP 404错误"                   │
│  - "GPT-4" 可能匹配不到 "GPT4" 或 "GPT 4"                   │
│  - 专有名词、缩写、代码片段匹配差                             │
│  - 精确匹配能力弱                                             │
│                                                             │
│  示例:                                                      │
│  查询: "Python IndexError"                                  │
│                                                             │
│  向量搜索可能返回:                                            │
│  1. "Python列表操作指南" (语义相关，但不是错误)                │
│  2. "数组越界错误处理" (语义相关，但不是Python)                │
│  3. "IndexError解决方法" (完美匹配)                          │
│                                                             │
│  关键词搜索会直接匹配:                                        │
│  1. "IndexError: list index out of range"                   │
│  2. "Python IndexError处理"                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 两种搜索方式对比

| 特性 | 向量搜索 | 关键词搜索 |
|------|---------|-----------|
| 语义理解 | 强 | 弱 |
| 关键词匹配 | 弱 | 强 |
| 同义词处理 | 好 | 差 |
| 精确匹配 | 差 | 好 |
| 计算开销 | 高 | 低 |
| 适用场景 | 自然语言查询 | 精确术语查询 |

---

## 2. BM25 关键词搜索

### TF-IDF 原理简述

```
┌─────────────────────────────────────────────────────────────┐
│              TF-IDF 原理                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TF (Term Frequency, 词频):                                 │
│  词在文档中出现的频率                                         │
│  TF(词, 文档) = 词在文档中出现次数 / 文档总词数               │
│                                                             │
│  示例:                                                      │
│  文档: "Python是一种编程语言，Python很流行"                    │
│  TF("Python") = 2/8 = 0.25                                 │
│                                                             │
│  IDF (Inverse Document Frequency, 逆文档频率):              │
│  衡量词的稀有程度                                             │
│  IDF(词) = log(总文档数 / 包含该词的文档数)                   │
│                                                             │
│  示例:                                                      │
│  总文档数: 1000                                             │
│  包含"Python"的文档: 100                                    │
│  IDF("Python") = log(1000/100) = 1                         │
│                                                             │
│  BM25 是 TF-IDF 的改进版本，考虑了文档长度等因素              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### rank_bm25 库使用

```python
from rank_bm25 import BM25Okapi
import jieba


def bm25_example():
    """BM25关键词搜索示例"""

    # 文档列表
    documents = [
        "Python是一种广泛使用的高级编程语言",
        "JavaScript是Web开发的核心语言",
        "机器学习是人工智能的一个分支",
        "深度学习使用神经网络进行模式识别",
        "Python在数据科学领域非常流行",
    ]

    # 中文分词
    tokenized_docs = [list(jieba.cut(doc)) for doc in documents]

    # 创建BM25索引
    bm25 = BM25Okapi(tokenized_docs)

    # 搜索
    query = "Python编程"
    tokenized_query = list(jieba.cut(query))

    # 获取相关性分数
    scores = bm25.get_scores(tokenized_query)

    # 按分数排序
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

    print(f"查询: {query}\n")
    for idx in ranked_indices[:3]:
        print(f"分数: {scores[idx]:.4f}")
        print(f"文档: {documents[idx]}")
        print()


if __name__ == "__main__":
    bm25_example()
```

### BM25 的特点

```python
"""
BM25的特点和使用场景
"""
from rank_bm25 import BM25Okapi


def bm25_features():
    """BM25特点演示"""

    # 示例1: 精确关键词匹配
    docs = [
        "HTTP 404 Not Found错误",
        "HTTP 500 Internal Server Error",
        "HTTP 403 Forbidden错误",
        "Python IndexError处理",
        "JavaScript TypeError解决",
    ]

    # 简单分词（英文按空格，中文需要用jieba）
    tokenized_docs = [doc.split() for doc in docs]
    bm25 = BM25Okapi(tokenized_docs)

    # 查询: 精确匹配"404"
    query = "404"
    scores = bm25.get_scores(query.split())

    print("查询: '404'")
    for i, (doc, score) in enumerate(zip(docs, scores)):
        if score > 0:
            print(f"  [{score:.4f}] {doc}")

    # 示例2: 多关键词匹配
    query = "HTTP Error"
    scores = bm25.get_scores(query.split())

    print("\n查询: 'HTTP Error'")
    for i, (doc, score) in enumerate(zip(docs, scores)):
        if score > 0:
            print(f"  [{score:.4f}] {doc}")


if __name__ == "__main__":
    bm25_features()
```

---

## 3. 混合搜索（Hybrid Search）

### 向量搜索 + BM25 关键词搜索

```
┌─────────────────────────────────────────────────────────────┐
│              混合搜索原理                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  用户查询: "Python装饰器怎么用"                               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 向量搜索                                            │   │
│  │ 语义理解: "Python装饰器" → 匹配相关概念               │   │
│  │ 结果: ["装饰器入门", "Python高级特性", ...]           │   │
│  └─────────────────────────────────────────────────────┘   │
│           │                                                 │
│           │    融合                                          │
│           ▼                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ BM25搜索                                            │   │
│  │ 关键词匹配: "Python", "装饰器" → 精确匹配             │   │
│  │ 结果: ["Python装饰器教程", "@decorator用法", ...]     │   │
│  └─────────────────────────────────────────────────────┘   │
│           │                                                 │
│           ▼                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 最终结果                                            │   │
│  │ 综合两种搜索的优势，返回最相关的结果                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### EnsembleRetriever

```python
"""
EnsembleRetriever 混合搜索示例
"""
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore


def create_hybrid_retriever(documents: list, index_name: str):
    """创建混合检索器"""

    # 1. 创建BM25检索器
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = 3  # 返回前3个结果

    # 2. 创建向量检索器
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings
    )
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 3. 创建混合检索器
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.4, 0.6]  # BM25权重0.4，向量权重0.6
    )

    return ensemble_retriever


def hybrid_search_example():
    """混合搜索示例"""

    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # 加载文档
    loader = TextLoader("data/documents.txt", encoding="utf-8")
    documents = loader.load()

    # 分块
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)

    # 创建混合检索器
    retriever = create_hybrid_retriever(chunks, "hybrid-index")

    # 搜索
    query = "Python装饰器怎么用"
    results = retriever.invoke(query)

    print(f"查询: {query}")
    print(f"找到 {len(results)} 个结果\n")

    for i, doc in enumerate(results, 1):
        print(f"结果 {i}:")
        print(f"  {doc.page_content[:200]}...")
        print()


if __name__ == "__main__":
    hybrid_search_example()
```

### 重要说明：LangChain 1.0 中的迁移

```
┌─────────────────────────────────────────────────────────────┐
│              LangChain 1.0 迁移说明                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  在 LangChain 1.0 中，EnsembleRetriever 已迁移到            │
│  langchain_classic 包:                                      │
│                                                             │
│  # 旧版本（LangChain 0.x）                                  │
│  from langchain.retrievers import EnsembleRetriever         │
│                                                             │
│  # 新版本（LangChain 1.0）                                  │
│  from langchain_classic.retrievers import EnsembleRetriever  │
│                                                             │
│  安装: pip install langchain-classic                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. 倒数排名融合（RRF）

### RRF 算法原理

```
┌─────────────────────────────────────────────────────────────┐
│              RRF (Reciprocal Rank Fusion) 原理               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  公式: RRF_score(d) = Σ 1 / (k + rank_i(d))                │
│                                                             │
│  其中:                                                      │
│  - d: 文档                                                  │
│  - k: 常数（通常为60）                                       │
│  - rank_i(d): 文档d在第i个检索器中的排名                     │
│                                                             │
│  示例:                                                      │
│  文档A在向量搜索中排名第1，在BM25中排名第3                   │
│  RRF_score(A) = 1/(60+1) + 1/(60+3) = 0.0164 + 0.0159      │
│               = 0.0323                                      │
│                                                             │
│  文档B在向量搜索中排名第3，在BM25中排名第1                   │
│  RRF_score(B) = 1/(60+3) + 1/(60+1) = 0.0159 + 0.0164      │
│               = 0.0323                                      │
│                                                             │
│  文档C在向量搜索中排名第2，在BM25中排名第2                   │
│  RRF_score(C) = 1/(60+2) + 1/(60+2) = 0.0161 + 0.0161      │
│               = 0.0322                                      │
│                                                             │
│  最终排名: A = B > C                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 为什么比简单加权更好

```
┌─────────────────────────────────────────────────────────────┐
│              RRF vs 简单加权                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  简单加权:                                                   │
│  final_score = w1 * vector_score + w2 * bm25_score          │
│                                                             │
│  问题:                                                      │
│  - 分数范围不同（向量分数0-1，BM25分数可能很大）              │
│  - 需要归一化处理                                             │
│  - 权重选择敏感                                               │
│                                                             │
│  RRF:                                                       │
│  final_score = Σ 1 / (k + rank_i)                           │
│                                                             │
│  优势:                                                      │
│  - 只关心排名，不关心分数                                     │
│  - 不需要归一化                                               │
│  - 对异常值不敏感                                             │
│  - 结果更稳定                                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### RRF 实现

```python
"""
RRF (Reciprocal Rank Fusion) 实现
"""
from typing import List, Dict


def reciprocal_rank_fusion(
    rankings: List[List[str]],
    k: int = 60
) -> List[tuple]:
    """
    倒数排名融合算法

    参数:
        rankings: 多个检索器的排名结果列表
        k: 常数，默认60

    返回:
        融合后的排名列表 [(doc_id, score), ...]
    """
    rrf_scores: Dict[str, float] = {}

    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, 1):
            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = 0.0
            rrf_scores[doc_id] += 1.0 / (k + rank)

    # 按分数降序排序
    sorted_results = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_results


def rrf_example():
    """RRF示例"""

    # 检索器1（向量搜索）的结果
    vector_results = ["doc_A", "doc_B", "doc_C", "doc_D"]

    # 检索器2（BM25搜索）的结果
    bm25_results = ["doc_C", "doc_A", "doc_E", "doc_B"]

    # 应用RRF
    rankings = [vector_results, bm25_results]
    fused_results = reciprocal_rank_fusion(rankings, k=60)

    print("向量搜索结果:", vector_results)
    print("BM25搜索结果:", bm25_results)
    print("\nRRF融合结果:")
    for doc_id, score in fused_results:
        print(f"  {doc_id}: {score:.6f}")


if __name__ == "__main__":
    rrf_example()
```

---

## 5. Chroma 向量存储

### 作为 Pinecone 的替代方案

```python
"""
Chroma 向量存储示例（本地替代Pinecone）
"""
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chroma_example():
    """Chroma向量存储示例"""

    # 1. 加载文档
    loader = TextLoader("data/documents.txt", encoding="utf-8")
    documents = loader.load()

    # 2. 分块
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)

    # 3. 初始化嵌入模型
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    # 4. 创建Chroma向量存储
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"  # 持久化目录
    )

    print(f"已存储 {len(chunks)} 个文档块到Chroma")

    # 5. 搜索
    query = "Python装饰器"
    results = vectorstore.similarity_search(query, k=3)

    print(f"\n查询: {query}")
    print(f"找到 {len(results)} 个结果\n")

    for i, doc in enumerate(results, 1):
        print(f"结果 {i}: {doc.page_content[:100]}...")

    return vectorstore


if __name__ == "__main__":
    chroma_example()
```

### Chroma vs Pinecone 对比

| 特性 | Chroma | Pinecone |
|------|--------|----------|
| 部署方式 | 本地/嵌入式 | 云服务 |
| 持久化 | 本地文件 | 云存储 |
| 成本 | 免费 | 免费层+付费 |
| 扩展性 | 单机 | 分布式 |
| 适用场景 | 开发/小规模 | 生产/大规模 |
| 配置复杂度 | 低 | 中 |

---

## 6. 混合搜索优化策略

### 权重配置优化

```python
"""
混合搜索权重优化
"""
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def optimize_weights(documents: list):
    """优化混合搜索权重"""

    # 创建检索器
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = 3

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(documents, embeddings)
    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # 测试不同权重组合
    weight_configs = [
        [0.3, 0.7],  # 偏向向量搜索
        [0.5, 0.5],  # 平均权重
        [0.7, 0.3],  # 偏向BM25
    ]

    test_queries = [
        "Python装饰器",           # 关键词明确
        "如何提高代码质量",       # 语义查询
        "HTTP 404错误处理",       # 精确术语
    ]

    for weights in weight_configs:
        print(f"\n权重配置: BM25={weights[0]}, Vector={weights[1]}")

        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, vector_retriever],
            weights=weights
        )

        for query in test_queries:
            results = ensemble_retriever.invoke(query)
            print(f"  查询 '{query}': {len(results)} 个结果")
```

### 查询预处理

```python
"""
查询预处理优化
"""
import re


def preprocess_query(query: str) -> str:
    """预处理查询"""

    # 1. 去除多余空格
    query = re.sub(r'\s+', ' ', query).strip()

    # 2. 处理特殊字符
    query = re.sub(r'[^\w\s一-鿿]', ' ', query)

    # 3. 去除停用词（简单示例）
    stop_words = {'的', '了', '是', '在', '和', '有', '这', '我', '你', '他'}
    words = query.split()
    words = [w for w in words if w not in stop_words]

    return ' '.join(words)


def query_expansion(query: str) -> list:
    """查询扩展（同义词）"""

    synonyms = {
        "Python": ["python", "py"],
        "错误": ["error", "exception", "bug"],
        "教程": ["tutorial", "指南", "入门"],
    }

    expanded = [query]

    for word, syns in synonyms.items():
        if word in query:
            for syn in syns:
                expanded.append(query.replace(word, syn))

    return expanded
```

---

## 7. 完整代码示例

### 示例1：完整的混合搜索 RAG 系统

```python
"""
完整的混合搜索RAG系统
"""
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


class HybridRAGSystem:
    """混合搜索RAG系统"""

    def __init__(self, persist_dir: str = "./hybrid_chroma_db"):
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        self.vectorstore = None
        self.bm25_retriever = None
        self.ensemble_retriever = None
        self.agent = None

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

        return chunks

    def create_retrievers(self, chunks: list):
        """创建混合检索器"""

        # 1. BM25检索器
        self.bm25_retriever = BM25Retriever.from_documents(chunks)
        self.bm25_retriever.k = 3

        # 2. 向量检索器
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        vector_retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )

        # 3. 混合检索器
        self.ensemble_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, vector_retriever],
            weights=[0.4, 0.6]  # BM25权重0.4，向量权重0.6
        )

        print("混合检索器创建完成")

    def create_agent(self):
        """创建RAG Agent"""

        @tool
        def search_knowledge_base(query: str) -> str:
            """
            搜索知识库，使用混合搜索（向量+关键词）查找相关文档。

            参数:
                query: 搜索查询

            返回:
                相关文档内容
            """
            results = self.ensemble_retriever.invoke(query)

            if not results:
                return "未找到相关文档"

            formatted = []
            for i, doc in enumerate(results[:3], 1):
                content = doc.page_content[:500]
                source = doc.metadata.get("source", "未知来源")
                formatted.append(f"文档{i} (来源: {source}):\n{content}")

            return "\n\n".join(formatted)

        model = init_chat_model("groq:llama-3.3-70b-versatile")
        checkpointer = InMemorySaver()

        self.agent = create_agent(
            model=model,
            tools=[search_knowledge_base],
            system_prompt="""你是知识库问答助手。

使用search_knowledge_base工具搜索相关文档，基于搜索结果回答问题。

回答要求：
1. 准确引用文档内容
2. 不要编造信息
3. 如果没有找到相关信息，如实告知""",
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

    # 创建系统
    rag = HybridRAGSystem()

    # 加载文档
    chunks = rag.load_documents("data/documents")

    # 创建检索器
    rag.create_retrievers(chunks)

    # 创建Agent
    rag.create_agent()

    # 交互式问答
    print("\n混合搜索RAG系统已就绪！")
    print("输入问题进行查询，输入'quit'退出\n")

    while True:
        question = input("问题: ")
        if question.lower() == "quit":
            break

        answer = rag.ask(question)
        print(f"\n回答: {answer}\n")


if __name__ == "__main__":
    main()
```

### 示例2：带RRF的混合搜索

```python
"""
带RRF的混合搜索示例
"""
from typing import List, Dict, Tuple
from langchain_community.retrievers import BM25Retriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


class RRFRetriever:
    """带RRF的混合检索器"""

    def __init__(
        self,
        documents: List[Document],
        k: int = 60,
        top_n: int = 5
    ):
        self.k = k
        self.top_n = top_n

        # BM25检索器
        self.bm25_retriever = BM25Retriever.from_documents(documents)
        self.bm25_retriever.k = 10  # 获取更多候选

        # 向量检索器
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(documents, embeddings)
        self.vector_retriever = vectorstore.as_retriever(
            search_kwargs={"k": 10}
        )

    def _rrf_score(
        self,
        rankings: List[List[Tuple[str, float]]]
    ) -> List[Tuple[str, float]]:
        """计算RRF分数"""

        rrf_scores: Dict[str, float] = {}

        for ranking in rankings:
            for rank, (doc_id, _) in enumerate(ranking, 1):
                if doc_id not in rrf_scores:
                    rrf_scores[doc_id] = 0.0
                rrf_scores[doc_id] += 1.0 / (self.k + rank)

        sorted_results = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_results[:self.top_n]

    def invoke(self, query: str) -> List[Document]:
        """执行混合搜索"""

        # 获取两个检索器的结果
        bm25_results = self.bm25_retriever.invoke(query)
        vector_results = self.vector_retriever.invoke(query)

        # 转换为排名格式
        bm25_ranking = [
            (doc.page_content[:100], 0) for doc in bm25_results
        ]
        vector_ranking = [
            (doc.page_content[:100], 0) for doc in vector_results
        ]

        # 应用RRF
        fused_rankings = self._rrf_score([bm25_ranking, vector_ranking])

        # 重建文档列表
        result_docs = []
        for doc_id, score in fused_rankings:
            # 找到原始文档
            for doc in bm25_results + vector_results:
                if doc.page_content[:100] == doc_id:
                    result_docs.append(doc)
                    break

        return result_docs


def rrf_retriever_example():
    """RRF检索器示例"""

    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    # 加载文档
    loader = TextLoader("data/documents.txt", encoding="utf-8")
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)

    # 创建RRF检索器
    retriever = RRFRetriever(chunks, k=60, top_n=5)

    # 搜索
    query = "Python装饰器"
    results = retriever.invoke(query)

    print(f"查询: {query}")
    print(f"找到 {len(results)} 个结果\n")

    for i, doc in enumerate(results, 1):
        print(f"结果 {i}: {doc.page_content[:100]}...")


if __name__ == "__main__":
    rrf_retriever_example()
```

---

## 8. 常见错误

### 错误1：未安装 langchain-classic

```python
# 错误：直接导入
from langchain.retrievers import EnsembleRetriever
# ImportError: cannot import name 'EnsembleRetriever'

# 正确：安装并从langchain_classic导入
# pip install langchain-classic
from langchain_classic.retrievers import EnsembleRetriever
```

### 错误2：权重配置错误

```python
# 错误：权重数量与检索器数量不匹配
EnsembleRetriever(
    retrievers=[bm25, vector, another],
    weights=[0.5, 0.5]  # 3个检索器但只有2个权重
)

# 正确：权重数量必须与检索器数量一致
EnsembleRetriever(
    retrievers=[bm25, vector, another],
    weights=[0.3, 0.4, 0.3]
)
```

### 错误3：BM25 中文分词问题

```python
# 错误：未使用分词直接创建BM25
bm25 = BM25Okapi(["Python是一种编程语言", "机器学习是AI分支"])
# 中文没有空格分隔，效果差

# 正确：使用jieba分词
import jieba
tokenized_docs = [list(jieba.cut(doc)) for doc in documents]
bm25 = BM25Okapi(tokenized_docs)
```

### 错误4：Chroma 持久化目录问题

```python
# 错误：每次运行都创建新的向量存储
vectorstore = Chroma.from_documents(chunks, embeddings)
# 没有persist_directory，数据不会持久化

# 正确：指定持久化目录
vectorstore = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./chroma_db"
)
```

---

## 9. 最佳实践

### 1. 根据场景选择搜索策略

```python
# 场景1: 自然语言查询为主 → 偏向向量搜索
weights = [0.3, 0.7]  # BM25=0.3, Vector=0.7

# 场景2: 精确术语查询为主 → 偏向BM25
weights = [0.7, 0.3]  # BM25=0.7, Vector=0.3

# 场景3: 混合查询 → 平均权重
weights = [0.5, 0.5]  # 平均
```

### 2. 使用RRF替代简单加权

```python
# 推荐使用RRF而不是简单加权
# RRF对异常值不敏感，结果更稳定
```

### 3. 优化BM25中文分词

```python
import jieba

# 添加自定义词典
jieba.load_userdict("custom_dict.txt")

# 精确模式分词
tokenized = list(jieba.cut(text, cut_all=False))
```

### 4. 定期重建索引

```python
def rebuild_index(vectorstore, documents: list):
    """重建向量索引"""
    # 删除旧索引
    vectorstore.delete_collection()

    # 创建新索引
    vectorstore = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory="./chroma_db"
    )

    return vectorstore
```

---

## 10. 练习题

### 练习1：BM25 搜索

实现一个BM25关键词搜索系统：
1. 使用rank_bm25库
2. 处理中文分词
3. 测试精确关键词匹配

### 练习2：混合搜索

实现一个混合搜索系统：
1. 创建BM25和向量两个检索器
2. 使用EnsembleRetriever组合
3. 测试不同权重配置

### 练习3：RRF 实现

实现RRF算法：
1. 手动实现RRF公式
2. 比较RRF与简单加权的效果
3. 测试不同k值的影响

### 练习4：完整的混合RAG

构建一个完整的混合搜索RAG系统：
1. 支持多文档加载
2. 使用BM25 + 向量混合搜索
3. 实现RAG Agent
4. 比较纯向量搜索与混合搜索的效果

---

[上一章：13-RAG基础](./13-RAG基础.md) | [返回目录](#目录) | [下一章：15-高级工具与Agent模式](./15-高级工具与Agent模式.md)
