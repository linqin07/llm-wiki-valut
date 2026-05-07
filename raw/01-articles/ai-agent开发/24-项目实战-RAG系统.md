# 24 - 项目实战：构建生产级 RAG 系统

## 目录

- [项目概述](#项目概述)
- [系统架构](#系统架构)
- [环境准备](#环境准备)
- [核心模块实现](#核心模块实现)
  - [文档加载器](#1-文档加载器)
  - [智能分块策略](#2-智能分块策略)
  - [向量存储与嵌入](#3-向量存储与嵌入)
  - [检索与重排](#4-检索与重排)
  - [对话式问答](#5-对话式问答)
- [完整项目代码](#完整项目代码)
- [部署与测试](#部署与测试)
- [性能优化](#性能优化)
- [常见错误](#常见错误)
- [最佳实践](#最佳实践)
- [练习题](#练习题)

---

## 项目概述

RAG（Retrieval-Augmented Generation，检索增强生成）是当前大语言模型应用中最重要的范式之一。它通过将外部知识库与 LLM 结合，解决了模型知识过时、幻觉（hallucination）等核心问题。

### 项目目标

本项目旨在构建一个**完整的生产级 RAG 系统**，具备以下能力：

1. **多格式文档处理**：支持 PDF、TXT、DOCX、CSV、HTML 等常见格式
2. **智能分块**：根据文档结构自适应选择分块策略
3. **高质量检索**：语义检索 + 关键词检索混合模式
4. **重排序（Reranking）**：对检索结果进行二次排序，提升相关性
5. **对话式问答**：支持多轮对话，带引用追踪和置信度评分
6. **可观测性**：完整的日志和性能监控

### 技术栈

| 组件 | 技术选择 | 说明 |
|------|---------|------|
| LLM 框架 | LangChain 1.0 | 核心编排框架 |
| 工作流引擎 | LangGraph 1.0 | 有状态工作流管理 |
| 向量存储 | Chroma | 本地持久化向量数据库 |
| 嵌入模型 | HuggingFace Embeddings | 本地运行，无需 API |
| 文档处理 | LangChain Document Loaders | 多格式支持 |
| 重排 | Cross-Encoder | 基于交叉编码器的重排序 |

---

## 系统架构

### 整体架构图

```
+================================================================+
|                      RAG 系统整体架构                            |
+================================================================+

  用户查询                                              用户
    |                                                    ^
    v                                                    |
+-----------+    +----------+    +---------+    +--------+--------+
| 意图识别   |--->| 查询改写  |--->| 检索路由 |-->|  响应生成         |
+-----------+    +----------+    +---------+    |  (带引用+置信度)  |
                                     |          +-----------------+
                                     v                ^
                              +-------------+         |
                              | 向量检索     |         |
                              | (语义+关键词) |         |
                              +-------------+         |
                                     |                |
                                     v                |
                              +-------------+         |
                              | 重排序       |---------+
                              | (Reranking)  |
                              +-------------+
                                     ^
                                     |
+================================================================+
|                      文档处理流水线                               |
+================================================================+

+--------+    +--------+    +---------+    +----------+    +------+
| 文档    |--->| 文本    |--->| 文本     |--->| 嵌入      |--->| 向量  |
| 加载    |    | 清洗    |    | 分块     |    | 生成      |    | 存储  |
+--------+    +--------+    +---------+    +----------+    +------+
  PDF          去噪           递归分块       HuggingFace     Chroma
  TXT          标准化         语义分块       Embeddings      持久化
  DOCX         元数据         重叠窗口
  CSV          提取
  HTML
```

### LangGraph 工作流图

```
                    +-------+
                    | START |
                    +---+---+
                        |
                        v
                +-------+--------+
                | 查询分析         |
                | (意图+改写)      |
                +-------+--------+
                        |
                        v
                +-------+--------+
                | 文档检索         |
                | (语义+关键词)    |
                +-------+--------+
                        |
                        v
                +-------+--------+
                | 重排序           |
                | (Cross-Encoder) |
                +-------+--------+
                        |
                        v
                +-------+--------+
                | 上下文组装       |
                +-------+--------+
                        |
                        v
                +-------+--------+
                | 回答生成         |
                | (带引用)        |
                +-------+--------+
                        |
                        v
                +-------+--------+
                | 质量评估         |
                +-------+---+----+
                    |       |
              满足   |       | 不满足
                    v       v
                +---+---+ +-+----------+
                |  END  | | 重新检索    |
                +-------+ | (改写查询)  |
                          +------------+
```

---

## 环境准备

### 依赖安装

```bash
# 核心依赖
pip install langchain>=1.0.0 langgraph>=1.0.0 langchain-core>=1.0.0

# 向量存储
pip install chromadb

# 文档加载器
pip install pypdf python-docx beautifulsoup4 pandas

# 嵌入模型（本地运行）
pip install sentence-transformers

# 可选：重排序模型
pip install cross-encoder
```

### 环境变量配置

```bash
# .env 文件
GROQ_API_KEY=your_groq_api_key_here
# 如果使用 OpenAI 嵌入（可选）
# OPENAI_API_KEY=your_openai_key_here
```

---

## 核心模块实现

### 1. 文档加载器

文档加载器负责将不同格式的文件统一转换为 LangChain 的 `Document` 对象。

```python
"""文档加载模块 - 支持多种文件格式"""

import os
from pathlib import Path
from typing import List
from langchain_core.documents import Document


class UniversalDocumentLoader:
    """通用文档加载器，支持多种文件格式"""

    # 支持的文件格式及对应的加载器
    SUPPORTED_FORMATS = {
        ".txt": "text",
        ".pdf": "pdf",
        ".docx": "docx",
        ".csv": "csv",
        ".html": "html",
        ".htm": "html",
        ".md": "text",
    }

    def __init__(self):
        self._loaders = {}

    def _get_loader(self, file_path: str, file_type: str):
        """根据文件类型获取对应的加载器"""
        if file_type == "text":
            from langchain_community.document_loaders import TextLoader
            return TextLoader(file_path, encoding="utf-8")

        elif file_type == "pdf":
            from langchain_community.document_loaders import PyPDFLoader
            return PyPDFLoader(file_path)

        elif file_type == "docx":
            from langchain_community.document_loaders import Docx2txtLoader
            return Docx2txtLoader(file_path)

        elif file_type == "csv":
            from langchain_community.document_loaders import CSVLoader
            return CSVLoader(file_path)

        elif file_type == "html":
            from langchain_community.document_loaders import BSHTMLLoader
            return BSHTMLLoader(file_path)

        else:
            raise ValueError(f"不支持的文件格式: {file_type}")

    def load_file(self, file_path: str) -> List[Document]:
        """加载单个文件"""
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"不支持的文件格式: {suffix}。"
                f"支持的格式: {list(self.SUPPORTED_FORMATS.keys())}"
            )

        file_type = self.SUPPORTED_FORMATS[suffix]
        loader = self._get_loader(file_path, file_type)
        documents = loader.load()

        # 添加元数据
        for doc in documents:
            doc.metadata.update({
                "source_file": str(path.name),
                "file_type": file_type,
                "file_size": path.stat().st_size,
            })

        print(f"[文档加载] 已加载 {path.name}: {len(documents)} 个文档片段")
        return documents

    def load_directory(self, dir_path: str) -> List[Document]:
        """加载目录下所有支持的文件"""
        all_documents = []
        path = Path(dir_path)

        for file_path in sorted(path.rglob("*")):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                try:
                    docs = self.load_file(str(file_path))
                    all_documents.extend(docs)
                except Exception as e:
                    print(f"[警告] 加载 {file_path.name} 失败: {e}")

        print(f"[文档加载] 共加载 {len(all_documents)} 个文档片段")
        return all_documents
```

**要点说明**：
- 使用工厂模式根据文件后缀选择加载器
- 为每个文档添加来源元数据，便于后续引用追踪
- 加载失败时跳过并警告，不影响整体流程

### 2. 智能分块策略

分块是 RAG 系统中最关键的环节之一。分块过大导致检索不精确，过小则丢失上下文。

```python
"""智能分块模块 - 自适应分块策略"""

from typing import List, Optional
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
    HTMLHeaderTextSplitter,
)


class SmartTextSplitter:
    """智能文本分块器，根据文档类型自适应选择策略"""

    # 默认分块参数
    DEFAULT_CHUNK_SIZE = 500
    DEFAULT_CHUNK_OVERLAP = 50

    def __init__(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _get_splitter_for_type(self, file_type: str):
        """根据文件类型选择分块策略"""
        if file_type == "markdown":
            # Markdown 按标题分块
            headers_to_split_on = [
                ("#", "标题1"),
                ("##", "标题2"),
                ("###", "标题3"),
            ]
            return MarkdownHeaderTextSplitter(
                headers_to_split_on=headers_to_split_on
            )

        elif file_type == "html":
            # HTML 按标签分块
            headers_to_split_on = [
                ("h1", "标题1"),
                ("h2", "标题2"),
                ("h3", "标题3"),
            ]
            return HTMLHeaderTextSplitter(
                headers_to_split_on=headers_to_split_on
            )

        else:
            # 通用递归字符分块
            return RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " "],
                length_function=len,
            )

    def split_documents(
        self,
        documents: List[Document],
        file_type: Optional[str] = None,
    ) -> List[Document]:
        """智能分块文档列表"""
        if not documents:
            return []

        # 自动检测文件类型
        if file_type is None:
            file_type = documents[0].metadata.get("file_type", "text")

        splitter = self._get_splitter_for_type(file_type)

        if file_type in ("markdown", "html"):
            # 这些分块器需要原始文本
            all_chunks = []
            for doc in documents:
                chunks = splitter.split_text(doc.page_content)
                for i, chunk in enumerate(chunks):
                    # 合并元数据
                    metadata = {**doc.metadata, **chunk.metadata}
                    metadata["chunk_index"] = i
                    all_chunks.append(Document(
                        page_content=chunk.page_content if hasattr(chunk, 'page_content') else str(chunk),
                        metadata=metadata,
                    ))
            return all_chunks
        else:
            # RecursiveCharacterTextSplitter 直接处理文档列表
            chunks = splitter.split_documents(documents)
            # 添加块索引
            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_index"] = i
            return chunks


def add_chunk_metadata(chunks: List[Document]) -> List[Document]:
    """为分块添加额外元数据"""
    for i, chunk in enumerate(chunks):
        # 计算块的字符数
        chunk.metadata["char_count"] = len(chunk.page_content)
        # 计算块的词数（中文按字符计，英文按空格分词）
        chunk.metadata["word_count"] = len(chunk.page_content.split())
        # 添加全局唯一 ID
        source = chunk.metadata.get("source_file", "unknown")
        chunk.metadata["chunk_id"] = f"{source}_chunk_{i}"

    return chunks
```

**分块策略对比**：

| 策略 | 适用场景 | chunk_size 建议 | 优缺点 |
|------|---------|----------------|--------|
| 递归字符分块 | 通用文本 | 500-1000 | 简单高效，但可能切断语义 |
| Markdown 标题分块 | Markdown 文档 | 按标题自动 | 保留文档结构 |
| 语义分块 | 高质量需求 | 动态 | 语义完整，但速度较慢 |

### 3. 向量存储与嵌入

```python
"""向量存储模块 - Chroma 向量数据库管理"""

import os
from typing import List, Optional
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore


class VectorStoreManager:
    """向量存储管理器"""

    def __init__(
        self,
        embedding_model: Optional[str] = None,
        persist_dir: str = "./chroma_db",
    ):
        self.persist_dir = persist_dir
        self._vectorstore = None
        self._embeddings = None
        self._embedding_model_name = embedding_model

    def _get_embeddings(self):
        """获取嵌入模型"""
        if self._embeddings is None:
            try:
                from langchain_huggingface import HuggingFaceEmbeddings
                model_name = self._embedding_model_name or "all-MiniLM-L6-v2"
                self._embeddings = HuggingFaceEmbeddings(
                    model_name=model_name,
                    model_kwargs={"device": "cpu"},
                    encode_kwargs={"normalize_embeddings": True},
                )
                print(f"[嵌入模型] 已加载: {model_name}")
            except ImportError:
                print("[警告] langchain_huggingface 未安装，使用 OpenAI 嵌入")
                from langchain_openai import OpenAIEmbeddings
                self._embeddings = OpenAIEmbeddings()
        return self._embeddings

    def create_from_documents(
        self,
        documents: List[Document],
        collection_name: str = "default",
    ) -> None:
        """从文档创建向量存储"""
        embeddings = self._get_embeddings()

        try:
            import chromadb
            from langchain_chroma import Chroma

            # 创建持久化客户端
            client = chromadb.PersistentClient(path=self.persist_dir)

            self._vectorstore = Chroma(
                client=client,
                collection_name=collection_name,
                embedding_function=embeddings,
            )

            # 添加文档
            self._vectorstore.add_documents(documents)
            print(f"[向量存储] 已创建集合 '{collection_name}'，包含 {len(documents)} 个文档")

        except ImportError:
            print("[回退] Chroma 未安装，使用内存向量存储")
            self._vectorstore = InMemoryVectorStore.from_documents(
                documents, embeddings
            )

    def load_existing(self, collection_name: str = "default") -> None:
        """加载已有的向量存储"""
        embeddings = self._get_embeddings()

        try:
            import chromadb
            from langchain_chroma import Chroma

            client = chromadb.PersistentClient(path=self.persist_dir)
            self._vectorstore = Chroma(
                client=client,
                collection_name=collection_name,
                embedding_function=embeddings,
            )
            print(f"[向量存储] 已加载集合 '{collection_name}'")

        except ImportError:
            raise RuntimeError("需要安装 chromadb 以加载已有向量存储")

    def get_retriever(
        self,
        search_type: str = "similarity",
        k: int = 4,
        score_threshold: Optional[float] = None,
    ):
        """获取检索器"""
        if self._vectorstore is None:
            raise RuntimeError("向量存储未初始化，请先调用 create_from_documents 或 load_existing")

        search_kwargs = {"k": k}
        if score_threshold is not None:
            search_kwargs["score_threshold"] = score_threshold

        return self._vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs=search_kwargs,
        )

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """直接执行相似性搜索"""
        if self._vectorstore is None:
            raise RuntimeError("向量存储未初始化")
        return self._vectorstore.similarity_search(query, k=k)

    def add_documents(self, documents: List[Document]) -> None:
        """向已有向量存储添加新文档"""
        if self._vectorstore is None:
            raise RuntimeError("向量存储未初始化")
        self._vectorstore.add_documents(documents)
        print(f"[向量存储] 已添加 {len(documents)} 个新文档")
```

### 4. 检索与重排

```python
"""检索与重排模块 - 提升检索质量"""

from typing import List, Tuple
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class HybridRetriever:
    """混合检索器：语义检索 + 可选的重排序"""

    def __init__(
        self,
        base_retriever: BaseRetriever,
        use_reranker: bool = True,
        reranker_top_k: int = 3,
    ):
        self.base_retriever = base_retriever
        self.use_reranker = use_reranker
        self.reranker_top_k = reranker_top_k
        self._cross_encoder = None

    def _get_cross_encoder(self):
        """加载交叉编码器用于重排序"""
        if self._cross_encoder is None:
            try:
                from sentence_transformers import CrossEncoder
                self._cross_encoder = CrossEncoder(
                    "cross-encoder/ms-marco-MiniLM-L-6-v2",
                    device="cpu",
                )
                print("[重排序器] Cross-Encoder 已加载")
            except ImportError:
                print("[警告] sentence_transformers 未安装，跳过重排序")
                self.use_reranker = False
        return self._cross_encoder

    def _rerank(
        self, query: str, documents: List[Document], top_k: int
    ) -> List[Document]:
        """使用交叉编码器对文档重排序"""
        if not documents:
            return []

        encoder = self._get_cross_encoder()
        if encoder is None or not self.use_reranker:
            return documents[:top_k]

        # 构建 query-document 对
        pairs = [(query, doc.page_content) for doc in documents]

        # 计算相关性分数
        scores = encoder.predict(pairs)

        # 按分数排序
        scored_docs = list(zip(scores, documents))
        scored_docs.sort(key=lambda x: x[0], reverse=True)

        # 返回 top_k 结果，并将分数写入元数据
        results = []
        for score, doc in scored_docs[:top_k]:
            doc.metadata["rerank_score"] = float(score)
            results.append(doc)

        return results

    def retrieve(self, query: str) -> List[Document]:
        """执行检索 + 重排序"""
        # 第一阶段：基础检索（获取较多候选）
        initial_k = self.reranker_top_k * 3  # 检索更多候选用于重排
        candidates = self.base_retriever.invoke(query)

        print(f"[检索] 初始检索到 {len(candidates)} 个候选文档")

        if self.use_reranker and len(candidates) > self.reranker_top_k:
            # 第二阶段：重排序
            results = self._rerank(query, candidates, self.reranker_top_k)
            print(f"[重排序] 筛选后保留 {len(results)} 个文档")
        else:
            results = candidates[:self.reranker_top_k]

        return results


def format_context(documents: List[Document]) -> str:
    """将检索到的文档格式化为上下文字符串"""
    if not documents:
        return "未找到相关文档。"

    context_parts = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source_file", "未知来源")
        score = doc.metadata.get("rerank_score", "")
        score_str = f" (相关度: {score:.3f})" if score else ""

        context_parts.append(
            f"[文档{i}] 来源: {source}{score_str}\n"
            f"{doc.page_content}\n"
        )

    return "\n---\n".join(context_parts)
```

### 5. 对话式问答

```python
"""对话式问答模块 - 支持多轮对话和引用追踪"""

from typing import List, TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.documents import Document
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


# ========== 状态定义 ==========
class RAGState(TypedDict):
    """RAG 系统状态"""
    messages: Annotated[list, add_messages]  # 对话历史
    context: str                              # 检索到的上下文
    sources: List[str]                        # 引用来源
    confidence: float                         # 置信度评分


# ========== 提示词模板 ==========
RAG_SYSTEM_PROMPT = """你是一个专业的知识问答助手。请根据以下检索到的文档内容回答用户问题。

规则：
1. 只根据提供的文档内容回答，不要编造信息
2. 如果文档中没有相关信息，请明确告知用户
3. 在回答中引用来源，格式为 [来源: 文件名]
4. 保持回答简洁、准确、有条理

检索到的文档内容：
{context}

引用来源：
{sources}
"""

# ========== 节点函数 ==========
def retrieve_node(state: RAGState, retriever=None) -> dict:
    """检索节点：根据用户最新问题检索相关文档"""
    # 获取最新用户消息
    last_message = state["messages"][-1]
    query = last_message.content if isinstance(last_message, HumanMessage) else ""

    # 执行检索
    documents = retriever.retrieve(query) if retriever else []

    # 格式化上下文
    context = format_context(documents)
    sources = list(set(
        doc.metadata.get("source_file", "未知") for doc in documents
    ))

    return {
        "context": context,
        "sources": sources,
    }


def generate_node(state: RAGState, llm=None) -> dict:
    """生成节点：根据上下文和对话历史生成回答"""
    # 构建完整的消息列表
    system_msg = SystemMessage(content=RAG_SYSTEM_PROMPT.format(
        context=state.get("context", ""),
        sources=", ".join(state.get("sources", [])),
    ))

    messages = [system_msg] + list(state["messages"])

    # 调用 LLM
    response = llm.invoke(messages)

    # 简单的置信度计算（基于是否有上下文）
    confidence = 0.8 if state.get("context") else 0.3

    return {
        "messages": [AIMessage(content=response.content)],
        "confidence": confidence,
    }


# ========== 图构建 ==========
def build_rag_graph(llm, retriever):
    """构建 RAG 工作流图"""
    graph = StateGraph(RAGState)

    # 添加节点（使用 lambda 包装以传入参数）
    graph.add_node("retrieve", lambda state: retrieve_node(state, retriever))
    graph.add_node("generate", lambda state: generate_node(state, llm))

    # 定义边
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
```

---

## 完整项目代码

### 项目文件结构

```
rag_system/
├── main.py              # 主入口
├── loader.py            # 文档加载器
├── splitter.py          # 文本分块器
├── vectorstore.py       # 向量存储管理
├── retriever.py         # 检索与重排
├── rag_graph.py         # LangGraph 工作流
├── config.py            # 配置管理
├── requirements.txt     # 依赖列表
├── data/                # 待索引的文档目录
│   ├── sample.pdf
│   └── sample.txt
└── chroma_db/           # Chroma 持久化目录
```

### config.py - 配置管理

```python
"""系统配置"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class RAGConfig:
    """RAG 系统配置"""
    # LLM 配置
    model_provider: str = "groq"
    model_name: str = "llama-3.3-70b-versatile"
    model_string: str = "groq:llama-3.3-70b-versatile"

    # 分块配置
    chunk_size: int = 500
    chunk_overlap: int = 50

    # 检索配置
    retrieval_k: int = 6          # 初始检索数量
    rerank_top_k: int = 3         # 重排后保留数量
    use_reranker: bool = True     # 是否使用重排序
    score_threshold: float = 0.3  # 相似度阈值

    # 嵌入配置
    embedding_model: str = "all-MiniLM-L6-v2"

    # 存储配置
    persist_dir: str = "./chroma_db"
    collection_name: str = "rag_collection"

    # 支持的文件格式
    supported_formats: List[str] = field(
        default_factory=lambda: [".txt", ".pdf", ".docx", ".csv", ".html"]
    )
```

### main.py - 主入口

```python
"""RAG 系统主入口"""

import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from config import RAGConfig
from loader import UniversalDocumentLoader
from splitter import SmartTextSplitter, add_chunk_metadata
from vectorstore import VectorStoreManager
from retriever import HybridRetriever
from rag_graph import build_rag_graph


def index_documents(config: RAGConfig, data_dir: str):
    """文档索引流水线"""
    print("=" * 60)
    print("开始文档索引...")
    print("=" * 60)

    # 1. 加载文档
    loader = UniversalDocumentLoader()
    documents = loader.load_directory(data_dir)
    if not documents:
        print("未找到任何文档，请检查 data 目录")
        return

    # 2. 分块
    splitter = SmartTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    chunks = add_chunk_metadata(chunks)
    print(f"[分块] 共生成 {len(chunks)} 个文本块")

    # 3. 创建向量存储
    store = VectorStoreManager(
        embedding_model=config.embedding_model,
        persist_dir=config.persist_dir,
    )
    store.create_from_documents(chunks, config.collection_name)

    print("=" * 60)
    print("文档索引完成！")
    print("=" * 60)
    return store


def create_rag_app(config: RAGConfig):
    """创建 RAG 应用"""
    # 初始化 LLM
    llm = init_chat_model(config.model_string)

    # 加载向量存储
    store = VectorStoreManager(
        embedding_model=config.embedding_model,
        persist_dir=config.persist_dir,
    )
    store.load_existing(config.collection_name)

    # 创建检索器
    base_retriever = store.get_retriever(k=config.retrieval_k)
    hybrid_retriever = HybridRetriever(
        base_retriever=base_retriever,
        use_reranker=config.use_reranker,
        reranker_top_k=config.rerank_top_k,
    )

    # 构建 RAG 图
    rag_graph = build_rag_graph(llm, hybrid_retriever)
    return rag_graph


def interactive_chat(rag_graph):
    """交互式对话"""
    print("\n" + "=" * 60)
    print("RAG 知识问答系统 (输入 'quit' 退出)")
    print("=" * 60 + "\n")

    while True:
        user_input = input("用户: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("再见！")
            break

        if not user_input:
            continue

        # 调用 RAG 图
        result = rag_graph.invoke({
            "messages": [HumanMessage(content=user_input)],
            "context": "",
            "sources": [],
            "confidence": 0.0,
        })

        # 输出回答
        ai_message = result["messages"][-1]
        print(f"\n助手: {ai_message.content}")

        # 输出引用来源
        if result.get("sources"):
            print(f"\n[引用来源: {', '.join(result['sources'])}]")
        if result.get("confidence"):
            print(f"[置信度: {result['confidence']:.2f}]")
        print()


if __name__ == "__main__":
    config = RAGConfig()

    # 检查是否需要索引
    data_dir = "./data"
    if os.path.exists(data_dir) and os.listdir(data_dir):
        index_documents(config, data_dir)

    # 启动对话
    rag_app = create_rag_app(config)

    from langchain_core.messages import HumanMessage
    interactive_chat(rag_app)
```

---

## 部署与测试

### 测试脚本

```python
"""RAG 系统测试"""

from langchain_core.messages import HumanMessage


def test_basic_qa(rag_graph):
    """测试基本问答"""
    test_questions = [
        "什么是 RAG？",
        "这个系统有哪些功能？",
        "如何优化检索效果？",
    ]

    for question in test_questions:
        print(f"\n问题: {question}")
        result = rag_graph.invoke({
            "messages": [HumanMessage(content=question)],
            "context": "",
            "sources": [],
            "confidence": 0.0,
        })
        answer = result["messages"][-1].content
        print(f"回答: {answer}")
        print(f"来源: {result.get('sources', [])}")
        print(f"置信度: {result.get('confidence', 0):.2f}")
        print("-" * 40)


def test_multi_turn(rag_graph):
    """测试多轮对话"""
    conversation = [
        "请介绍一下 LangChain 框架",
        "它和 LangGraph 有什么区别？",
        "在实际项目中应该怎么选择？",
    ]

    messages = []
    for question in conversation:
        messages.append(HumanMessage(content=question))
        result = rag_graph.invoke({
            "messages": messages,
            "context": "",
            "sources": [],
            "confidence": 0.0,
        })
        answer = result["messages"][-1].content
        messages.append(result["messages"][-1])
        print(f"\n用户: {question}")
        print(f"助手: {answer[:200]}...")
```

---

## 性能优化

### 1. 分块策略优化

```python
# 根据文档类型选择最优分块参数
CHUNK_CONFIGS = {
    "technical": {"chunk_size": 800, "chunk_overlap": 100},
    "narrative": {"chunk_size": 1000, "chunk_overlap": 150},
    "code":      {"chunk_size": 300, "chunk_overlap": 50},
    "table":     {"chunk_size": 2000, "chunk_overlap": 0},
}
```

### 2. 检索优化

| 优化策略 | 效果 | 复杂度 |
|---------|------|--------|
| 混合检索（语义+关键词） | 提升召回率 15-25% | 中 |
| 重排序 | 提升精确率 10-20% | 低 |
| 查询改写 | 提升模糊查询效果 20-30% | 中 |
| HyDE（假设文档嵌入） | 提升语义匹配 10-15% | 高 |

### 3. 缓存策略

```python
from functools import lru_cache
from langchain_core.globals import set_llm_cache
from langchain_community.cache import InMemoryCache

# 启用 LLM 响应缓存
set_llm_cache(InMemoryCache())

# 或使用 SQLite 持久化缓存
# from langchain_community.cache import SQLiteCache
# set_llm_cache(SQLiteCache(database_path=".langchain.db"))
```

---

## 常见错误

### 1. 嵌入模型下载失败

```
错误: OSError: Can't load tokenizer for 'all-MiniLM-L6-v2'
```

**解决方案**：
```bash
# 手动下载模型
pip install huggingface_hub
python -c "from huggingface_hub import snapshot_download; snapshot_download('sentence-transformers/all-MiniLM-L6-v2')"

# 或使用国内镜像
export HF_ENDPOINT=https://hf-mirror.com
```

### 2. Chroma 版本兼容问题

```
错误: TypeError: expected str, bytes or os.PathLike object, not NoneType
```

**解决方案**：确保使用正确的 Chroma API：
```python
# 正确写法
import chromadb
client = chromadb.PersistentClient(path="./chroma_db")  # path 不能为空
```

### 3. 上下文窗口超限

```
错误: This model's maximum context length is 8192 tokens
```

**解决方案**：
```python
# 减少检索数量或截断上下文
config.retrieval_k = 3          # 从 6 减到 3
config.rerank_top_k = 2         # 从 3 减到 2
config.chunk_size = 300         # 从 500 减到 300
```

---

## 最佳实践

1. **分块大小选择**：从 500 字符开始测试，根据检索效果调整
2. **重排序值得使用**：即使增加少量延迟，也能显著提升质量
3. **元数据很重要**：始终保留文档来源信息，便于引用追踪
4. **增量索引**：文档更新时只重新索引变更部分，避免全量重建
5. **评估驱动开发**：建立测试问答对，用准确率指导优化方向
6. **监控生产指标**：追踪检索延迟、LLM 调用次数、用户满意度
7. **优雅降级**：检索失败时应有兜底策略，而非直接报错

---

## 练习题

### 基础练习

1. **单格式 RAG**：使用纯 TXT 文件构建一个最简单的 RAG 系统，理解完整流程
2. **分块实验**：对同一篇文档分别使用 chunk_size=200/500/1000，比较检索效果
3. **检索对比**：分别使用相似性搜索和 MMR（最大边际相关性）搜索，观察结果差异

### 进阶练习

4. **添加查询改写**：在检索前使用 LLM 改写用户查询，提升检索质量
5. **实现引用高亮**：在回答中标注具体引用的文档片段位置
6. **添加 Web 界面**：使用 Gradio 或 Streamlit 为 RAG 系统添加 Web 界面

### 挑战练习

7. **混合检索**：同时使用语义检索和 BM25 关键词检索，合并结果
8. **评估框架**：构建自动评估流水线，计算检索准确率和回答质量
9. **生产部署**：将系统容器化（Docker），并实现 API 接口

---

> **下一章**：[25 - 项目实战：多Agent客服系统](./25-项目实战-多Agent客服.md)
