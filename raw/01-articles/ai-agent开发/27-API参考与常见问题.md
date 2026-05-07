# 27 - API 参考手册与常见问题

## 目录

- [API 速查表](#api-速查表)
  - [模型初始化](#1-模型初始化)
  - [Agent 创建](#2-agent-创建)
  - [消息类型](#3-消息类型)
  - [提示词模板](#4-提示词模板)
  - [工具定义](#5-工具定义)
  - [状态图](#6-状态图)
  - [检查点](#7-检查点)
  - [中间件](#8-中间件)
  - [结构化输出](#9-结构化输出)
  - [文档加载器](#10-文档加载器)
  - [文本分块](#11-文本分块)
  - [向量存储](#12-向量存储)
  - [嵌入模型](#13-嵌入模型)
  - [检索器](#14-检索器)
- [常见错误与解决方案](#常见错误与解决方案)
- [迁移指南](#迁移指南)
- [性能优化建议](#性能优化建议)
- [学习资源](#学习资源)

---

## API 速查表

### 1. 模型初始化

`init_chat_model()` 是 LangChain 1.0 推荐的统一模型初始化函数，通过 provider 前缀自动选择后端。

```python
from langchain.chat_models import init_chat_model

# Groq（推荐，免费额度）
model = init_chat_model("groq:llama-3.3-70b-versatile")

# OpenAI
model = init_chat_model("openai:gpt-4o")

# Anthropic
model = init_chat_model("anthropic:claude-sonnet-4-20250514")

# 带参数初始化
model = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    temperature=0.7,       # 创造性（0=确定性，1=随机）
    max_tokens=2048,       # 最大输出 token 数
    timeout=30,            # 请求超时（秒）
)
```

**常用模型参数**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `temperature` | float | 0.7 | 控制输出随机性，0 最确定，1 最随机 |
| `max_tokens` | int | 模型默认 | 最大输出 token 数 |
| `timeout` | float | 无 | 请求超时秒数 |
| `max_retries` | int | 2 | 失败重试次数 |
| `streaming` | bool | False | 是否启用流式输出 |

### 2. Agent 创建

LangChain 1.0 使用 `create_agent()` 替代旧版的 `create_react_agent()`。

```python
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """搜索互联网信息。"""
    return f"搜索结果: {query}"

# 基本创建
agent = create_agent(
    model=model,
    tools=[search],
    system_prompt="你是一个有帮助的助手。",
)

# 调用 Agent
response = agent.invoke({
    "messages": [{"role": "user", "content": "你好"}],
})

# 获取回答
answer = response["messages"][-1].content

# 异步调用
response = await agent.ainvoke({
    "messages": [{"role": "user", "content": "你好"}],
})

# 流式调用
async for event in agent.astream({
    "messages": [{"role": "user", "content": "你好"}],
}):
    print(event)
```

**create_agent() 参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | BaseChatModel | 是 | 语言模型实例 |
| `tools` | list[Tool] | 否 | 工具列表，默认空列表 |
| `system_prompt` | str | 否 | 系统提示词 |
| `checkpointer` | BaseCheckpointSaver | 否 | 状态检查点 |

### 3. 消息类型

LangChain 使用统一的消息类型系统在不同角色之间传递信息。

```python
from langchain_core.messages import (
    HumanMessage,    # 用户消息
    AIMessage,       # AI 回复
    SystemMessage,   # 系统提示
    ToolMessage,     # 工具返回结果
)

# 创建消息（方式一：直接实例化）
msg = HumanMessage(content="你好")

# 创建消息（方式二：字典格式）
msg = {"role": "user", "content": "你好"}

# 带附加信息的消息
msg = HumanMessage(
    content="分析这张图片",
    # 多模态内容
    content=[
        {"type": "text", "text": "分析这张图片"},
        {"type": "image_url", "image_url": {"url": "https://..."}},
    ],
)

# ToolMessage - 工具调用的返回结果
tool_msg = ToolMessage(
    content="搜索结果: ...",
    tool_call_id="call_abc123",  # 必须与 AIMessage 中的 tool_call id 匹配
)

# AIMessage 中的工具调用
ai_msg = AIMessage(
    content="",
    tool_calls=[{
        "id": "call_abc123",
        "name": "search",
        "args": {"query": "LangChain 1.0"},
    }],
)
```

**消息类型一览**：

| 类型 | 角色 | 典型用途 |
|------|------|---------|
| `SystemMessage` | system | 设定助手行为、人格、规则 |
| `HumanMessage` | user | 用户的输入消息 |
| `AIMessage` | assistant | AI 的回复，可能包含工具调用 |
| `ToolMessage` | tool | 工具执行后的返回结果 |

### 4. 提示词模板

```python
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)

# ========== PromptTemplate（纯文本模板） ==========
template = PromptTemplate.from_template(
    "请将以下文本翻译为{language}：\n{text}"
)
result = template.invoke({"language": "英文", "text": "你好世界"})
# -> "请将以下文本翻译为英文：\n你好世界"

# ========== ChatPromptTemplate（聊天模板） ==========
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，请用{style}的风格回答。"),
    ("user", "{question}"),
])

messages = chat_prompt.invoke({
    "role": "翻译专家",
    "style": "简洁",
    "question": "什么是 RAG？",
})

# ========== MessagesPlaceholder（插入消息列表） ==========
prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", "你是一个有帮助的助手。"),
    MessagesPlaceholder("history"),  # 插入对话历史
    ("user", "{input}"),
])

result = prompt_with_history.invoke({
    "history": [
        HumanMessage(content="我叫张三"),
        AIMessage(content="你好，张三！"),
    ],
    "input": "我叫什么名字？",
})
```

### 5. 工具定义

```python
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field

# ========== @tool 装饰器（推荐方式） ==========
@tool
def multiply(a: int, b: int) -> int:
    """将两个整数相乘并返回结果。

    Args:
        a: 第一个乘数
        b: 第二个乘数
    """
    return a * b

# 调用工具
result = multiply.invoke({"a": 3, "b": 4})  # -> 12

# ========== 带复杂参数的工具 ==========
class SearchInput(BaseModel):
    """搜索参数"""
    query: str = Field(description="搜索关键词")
    max_results: int = Field(default=5, description="最大结果数", ge=1, le=20)

@tool(args_schema=SearchInput)
def advanced_search(query: str, max_results: int = 5) -> str:
    """执行高级搜索。"""
    return f"搜索 '{query}'，返回 {max_results} 条结果"

# ========== StructuredTool（显式定义） ==========
class CalculatorInput(BaseModel):
    expression: str = Field(description="数学表达式")

calculator = StructuredTool.from_function(
    func=lambda expression: str(eval(expression)),
    name="calculator",
    description="计算数学表达式",
    args_schema=CalculatorInput,
)

# ========== bind_tools() - 将工具绑定到模型 ==========
model_with_tools = model.bind_tools([multiply, advanced_search])

# 模型会自动决定是否调用工具
response = model_with_tools.invoke("3 乘以 4 等于多少？")
# response.tool_calls -> [{"name": "multiply", "args": {"a": 3, "b": 4}, ...}]
```

### 6. 状态图

LangGraph 的核心 API，用于构建有状态的工作流。

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# ========== 状态定义 ==========
class MyState(TypedDict):
    # 使用 add_messages 注解自动追加消息
    messages: Annotated[list, add_messages]
    # 普通字段，直接覆盖
    counter: int
    data: dict

# ========== 创建图 ==========
graph = StateGraph(MyState)

# ========== 添加节点 ==========
def node_a(state: MyState) -> dict:
    """节点处理函数，返回状态更新"""
    return {"counter": state["counter"] + 1}

def node_b(state: MyState) -> dict:
    return {"counter": state["counter"] * 2}

graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)

# ========== 添加边 ==========
# 普通边：A -> B
graph.add_edge(START, "node_a")    # 起始 -> A
graph.add_edge("node_a", "node_b") # A -> B
graph.add_edge("node_b", END)      # B -> 结束

# 条件边：根据函数返回值决定下一步
def decide_next(state: MyState) -> str:
    if state["counter"] > 10:
        return "node_b"
    return END

graph.add_conditional_edges(
    "node_a",           # 源节点
    decide_next,        # 路由函数
    {                   # 返回值 -> 目标节点的映射
        "node_b": "node_b",
        END: END,
    },
)

# ========== 编译并运行 ==========
app = graph.compile()
result = app.invoke({"messages": [], "counter": 0, "data": {}})
```

**状态图 API 汇总**：

| API | 说明 |
|-----|------|
| `StateGraph(StateType)` | 创建状态图，StateType 为 TypedDict |
| `graph.add_node(name, func)` | 添加节点 |
| `graph.add_edge(start, end)` | 添加普通边 |
| `graph.add_conditional_edges(source, func, mapping)` | 添加条件边 |
| `graph.compile()` | 编译图为可执行应用 |
| `START` | 起始节点常量 |
| `END` | 结束节点常量 |
| `add_messages` | 消息列表的 reducer，自动追加而非覆盖 |

### 7. 检查点

检查点用于持久化图的状态，支持对话历史保存和断点续执行。

```python
from langgraph.checkpoint.memory import InMemorySaver

# ========== 内存检查点（开发/测试用） ==========
checkpointer = InMemorySaver()

# 创建带检查点的图
app = graph.compile(checkpointer=checkpointer)

# 使用 thread_id 进行多轮对话
config = {"configurable": {"thread_id": "user_123"}}

# 第一轮
result1 = app.invoke(
    {"messages": [{"role": "user", "content": "我叫张三"}]},
    config=config,
)

# 第二轮（自动加载历史）
result2 = app.invoke(
    {"messages": [{"role": "user", "content": "我叫什么？"}]},
    config=config,
)

# ========== SQLite 检查点（持久化） ==========
# 需要安装: pip install langgraph-checkpoint-sqlite
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("./checkpoints.db")
app = graph.compile(checkpointer=checkpointer)

# ========== 获取历史状态 ==========
# 获取某个 thread 的所有历史状态
history = list(checkpointer.list(config))
for state in history:
    print(state)
```

### 8. 中间件

中间件在 Agent 执行过程中注入自定义逻辑。

```python
from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware import SummarizationMiddleware

# ========== 自定义中间件 ==========
class LoggingMiddleware(AgentMiddleware):
    """日志中间件 - 记录每次工具调用"""

    async def on_tool_start(self, tool_name, tool_input, **kwargs):
        print(f"[工具调用开始] {tool_name}({tool_input})")

    async def on_tool_end(self, tool_name, tool_output, **kwargs):
        print(f"[工具调用结束] {tool_name} -> {tool_output[:100]}")

    async def on_agent_finish(self, response, **kwargs):
        print(f"[Agent 完成] {response.content[:100]}")

# 使用中间件
agent = create_agent(
    model=model,
    tools=[search],
    system_prompt="你是一个助手。",
    middleware=[LoggingMiddleware()],
)

# ========== 摘要中间件（管理长对话） ==========
summarizer = SummarizationMiddleware(
    model=model,
    max_messages=20,         # 超过 20 条消息时触发摘要
    summary_prompt="请简要总结以上对话的要点。",
)

agent = create_agent(
    model=model,
    tools=[search],
    system_prompt="你是一个助手。",
    middleware=[summarizer],
)
```

### 9. 结构化输出

让 LLM 返回符合指定 Schema 的结构化数据。

```python
from pydantic import BaseModel, Field
from typing import Optional

# ========== 定义输出 Schema ==========
class PersonInfo(BaseModel):
    """人物信息"""
    name: str = Field(description="姓名")
    age: int = Field(description="年龄", ge=0, le=150)
    occupation: str = Field(description="职业")
    skills: list[str] = Field(description="技能列表")
    bio: Optional[str] = Field(default=None, description="简介")

# ========== 使用 with_structured_output ==========
structured_llm = model.with_structured_output(PersonInfo)

result = structured_llm.invoke("我叫李明，28岁，是个 Python 开发者，擅长 Django 和 FastAPI")
print(result.name)       # -> "李明"
print(result.age)        # -> 28
print(result.skills)     # -> ["Django", "FastAPI"]

# ========== 枚举类型 ==========
from enum import Enum

class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class SentimentResult(BaseModel):
    sentiment: Sentiment
    confidence: float = Field(ge=0.0, le=1.0)

structured_llm = model.with_structured_output(SentimentResult)
result = structured_llm.invoke("这个产品太棒了！")
print(result.sentiment)  # -> Sentiment.POSITIVE
```

### 10. 文档加载器

```python
# ========== 纯文本 ==========
from langchain_community.document_loaders import TextLoader
loader = TextLoader("data.txt", encoding="utf-8")
docs = loader.load()  # -> [Document(page_content="...", metadata={...})]

# ========== PDF ==========
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("document.pdf")
docs = loader.load()  # 每页一个 Document

# ========== CSV ==========
from langchain_community.document_loaders import CSVLoader
loader = CSVLoader("data.csv")
docs = loader.load()

# ========== HTML ==========
from langchain_community.document_loaders import BSHTMLLoader
loader = BSHTMLLoader("page.html")
docs = loader.load()

# ========== DOCX ==========
from langchain_community.document_loaders import Docx2txtLoader
loader = Docx2txtLoader("document.docx")
docs = loader.load()

# ========== 目录批量加载 ==========
from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader(
    "./docs",
    glob="**/*.txt",       # 匹配模式
    loader_cls=TextLoader,  # 使用的加载器
    show_progress=True,
)
docs = loader.load()

# ========== Document 对象结构 ==========
# docs[0].page_content  -> 文本内容
# docs[0].metadata       -> {"source": "file.txt", "page": 0, ...}
```

### 11. 文本分块

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

# ========== 递归字符分块（推荐） ==========
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,         # 每块最大字符数
    chunk_overlap=50,       # 块间重叠字符数
    separators=["\n\n", "\n", "。", "！", "？", ".", " "],
    length_function=len,
)

# 分块文本
chunks = splitter.split_text("很长的文本...")

# 分块文档
from langchain_core.documents import Document
docs = [Document(page_content="很长的文本...")]
chunked_docs = splitter.split_documents(docs)

# ========== Markdown 标题分块 ==========
headers_to_split_on = [
    ("#", "标题1"),
    ("##", "标题2"),
    ("###", "标题3"),
]
md_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on,
)
chunks = md_splitter.split_text("# 标题\n\n内容\n\n## 子标题\n\n子内容")

# 分块参数建议
CHUNK_RECOMMENDATIONS = {
    "通用文本":   {"chunk_size": 500, "chunk_overlap": 50},
    "技术文档":   {"chunk_size": 800, "chunk_overlap": 100},
    "代码文件":   {"chunk_size": 300, "chunk_overlap": 30},
    "对话记录":   {"chunk_size": 1000, "chunk_overlap": 150},
}
```

### 12. 向量存储

```python
# ========== 内存向量存储（开发测试） ==========
from langchain_core.vectorstores import InMemoryVectorStore

vectorstore = InMemoryVectorStore.from_documents(documents, embeddings)

# 添加文档
vectorstore.add_documents(new_docs)

# 相似性搜索
results = vectorstore.similarity_search("查询文本", k=4)

# 带分数的搜索
results_with_scores = vectorstore.similarity_search_with_score("查询文本", k=4)
# -> [(Document, float_score), ...]

# 获取检索器
retriever = vectorstore.as_retriever(
    search_type="similarity",    # 或 "mmr"（最大边际相关性）
    search_kwargs={"k": 4},
)

# ========== Chroma（持久化） ==========
# pip install chromadb langchain-chroma
import chromadb
from langchain_chroma import Chroma

client = chromadb.PersistentClient(path="./chroma_db")
chroma_store = Chroma(
    client=client,
    collection_name="my_collection",
    embedding_function=embeddings,
)
chroma_store.add_documents(documents)
results = chroma_store.similarity_search("查询")

# ========== MMR 搜索（增加多样性） ==========
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5},
)
```

### 13. 嵌入模型

```python
# ========== HuggingFace 本地嵌入（推荐，无需 API） ==========
# pip install langchain-huggingface sentence-transformers
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",    # 轻量模型，速度快
    model_kwargs={"device": "cpu"},    # 使用 CPU
    encode_kwargs={"normalize_embeddings": True},
)

# 嵌入单个文本
vector = embeddings.embed_query("你好世界")
# -> [0.0123, -0.0456, ...]  (384 维向量)

# 嵌入多个文本
vectors = embeddings.embed_documents(["文本1", "文本2", "文本3"])

# ========== OpenAI 嵌入 ==========
from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# ========== 推荐嵌入模型 ==========
EMBEDDING_MODELS = {
    "all-MiniLM-L6-v2":     "轻量快速，384维，适合开发测试",
    "all-mpnet-base-v2":     "高质量，768维，适合生产",
    "bge-small-zh-v1.5":     "中文优化，512维",
    "text-embedding-3-small": "OpenAI，1536维，需 API",
}
```

### 14. 检索器

```python
# ========== 基础检索器 ==========
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 使用检索器
docs = retriever.invoke("查询文本")

# ========== EnsembleRetriever（混合检索） ==========
# 注意：EnsembleRetriever 在 langchain_classic 中
from langchain_classic.retrievers import EnsembleRetriever

# 需要安装 rank_bm25: pip install rank_bm25
from langchain_community.retrievers import BM25Retriever

# BM25 关键词检索器
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 4

# 向量检索器
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 混合检索
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7],  # BM25 权重 30%，向量权重 70%
)

results = ensemble_retriever.invoke("查询文本")

# ========== 自定义检索器 ==========
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document

class CustomRetriever(BaseRetriever):
    """自定义检索器"""

    def _get_relevant_documents(self, query: str) -> list[Document]:
        # 实现自定义检索逻辑
        return [Document(page_content=f"结果: {query}")]
```

---

## 常见错误与解决方案

### 1. API Key 相关错误

**错误信息**：
```
AuthenticationError: Incorrect API key provided
```

**解决方案**：
```python
# 方案一：.env 文件
# .env 文件中写入
GROQ_API_KEY=gsk_xxxxxxxxxxxx

# Python 中加载
from dotenv import load_dotenv
load_dotenv()

# 方案二：环境变量
import os
os.environ["GROQ_API_KEY"] = "gsk_xxxxxxxxxxxx"

# 方案三：直接传参（不推荐，容易泄露）
model = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    api_key="gsk_xxxxxxxxxxxx",
)
```

**排查清单**：
- [ ] `.env` 文件是否在项目根目录
- [ ] 是否调用了 `load_dotenv()`
- [ ] API Key 是否有多余空格或换行
- [ ] API Key 是否过期

### 2. 导入路径错误

**错误信息**：
```
ImportError: cannot import name 'create_react_agent' from 'langchain.agents'
```

**原因**：LangChain 1.0 重命名了 API。

**解决方案**：
```python
# 旧版（LangChain 0.x）
from langchain.agents import create_react_agent

# 新版（LangChain 1.0）
from langchain.agents import create_agent

# 如果需要兼容旧代码
try:
    from langchain.agents import create_agent
except ImportError:
    from langgraph.prebuilt import create_react_agent as create_agent
```

**常见导入路径对照表**：

| 旧版 (0.x) | 新版 (1.0) |
|------------|-----------|
| `langgraph.prebuilt.create_react_agent` | `langchain.agents.create_agent` |
| `langchain_community.retrievers.EnsembleRetriever` | `langchain_classic.retrievers.EnsembleRetriever` |
| `langchain.chat_models.ChatOpenAI` | `init_chat_model("openai:...")` |

### 3. Groq Unicode 问题

**错误信息**：
```
UnicodeEncodeError: 'charmap' codec can't encode characters
```

**原因**：Windows 默认编码不支持某些 Unicode 字符。

**解决方案**：
```python
# 方案一：设置环境变量
import os
os.environ["PYTHONIOENCODING"] = "utf-8"

# 方案二：在脚本开头设置
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 方案三：Windows 终端设置
# 在 PowerShell 中执行: $env:PYTHONUTF8=1
```

### 4. 上下文窗口超限

**错误信息**：
```
BadRequestError: This model's maximum context length is 8192 tokens
```

**解决方案**：
```python
# 方案一：减少输入长度
# - 缩短系统提示词
# - 减少对话历史轮数
# - 减少检索文档数量

# 方案二：使用摘要中间件
from langchain.agents.middleware import SummarizationMiddleware
middleware = SummarizationMiddleware(model=model, max_messages=10)

# 方案三：截断长文本
def truncate_text(text: str, max_tokens: int = 4000) -> str:
    """粗略截断文本到指定 token 数"""
    chars_per_token = 4  # 中文约 2-3，英文约 4
    max_chars = max_tokens * chars_per_token
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[内容已截断]"
    return text
```

### 5. 工具调用失败

**错误信息**：
```
ToolException: Tool 'xxx' expects parameter 'yyy' but received 'zzz'
```

**解决方案**：
```python
# 确保工具定义清晰
@tool
def my_tool(param1: str, param2: int = 10) -> str:
    """工具的详细描述。

    Args:
        param1: 第一个参数的说明，必须是字符串
        param2: 第二个参数的说明，默认值为 10
    """
    # 类型验证
    if not isinstance(param1, str):
        raise ValueError("param1 必须是字符串")
    return f"结果: {param1}, {param2}"
```

### 6. 检查点文件锁定

**错误信息**：
```
sqlite3.OperationalError: database is locked
```

**解决方案**：
```python
# 方案一：使用内存检查点（开发环境）
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

# 方案二：确保单线程写入
import sqlite3
conn = sqlite3.connect("checkpoints.db", timeout=30)

# 方案三：使用 WAL 模式
conn.execute("PRAGMA journal_mode=WAL")
```

### 7. 结构化输出验证失败

**错误信息**：
```
pydantic.ValidationError: 1 validation error for MyModel
```

**解决方案**：
```python
# 确保 Pydantic 模型的 description 清晰明确
class MyModel(BaseModel):
    # 不好的描述
    name: str = Field(description="名字")

    # 好的描述
    name: str = Field(
        description="用户的全名，格式为中文姓名，如'张三'或'李小明'"
    )

    # 使用默认值处理可能缺失的字段
    optional_field: str = Field(
        default="未知",
        description="可选字段，如果无法确定则使用默认值"
    )

    # 使用枚举限制取值范围
    status: Literal["active", "inactive"] = Field(
        description="状态，只能是 active 或 inactive"
    )
```

### 8. 异步事件循环冲突

**错误信息**：
```
RuntimeError: This event loop is already running
```

**解决方案**：
```python
# 方案一：使用 asyncio.run()（推荐）
import asyncio

async def main():
    result = await agent.ainvoke({...})
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

# 方案二：Jupyter Notebook 中使用 nest_asyncio
# pip install nest_asyncio
import nest_asyncio
nest_asyncio.apply()

# 然后可以直接 await
result = await agent.ainvoke({...})

# 方案三：使用同步接口
result = agent.invoke({...})  # 同步调用，不需要 await
```

---

## 迁移指南

### 从 LangChain 0.x 迁移到 1.0

#### Agent 创建迁移

```python
# ============ 旧版 ============
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=model,
    tools=tools,
)

response = agent.invoke({"messages": [HumanMessage(content="你好")]})

# ============ 新版 ============
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="你是一个助手。",  # 新增：直接传入系统提示
)

response = agent.invoke({"messages": [{"role": "user", "content": "你好"}]})
```

**主要变化**：
1. 导入路径从 `langgraph.prebuilt` 改为 `langchain.agents`
2. 函数名从 `create_react_agent` 改为 `create_agent`
3. 新增 `system_prompt` 参数，无需额外构造 SystemMessage
4. 消息格式更灵活，支持字典格式

#### 模型初始化迁移

```python
# ============ 旧版 ============
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

model = ChatOpenAI(model="gpt-4o", temperature=0.7)
model = ChatAnthropic(model="claude-3-opus-20240229")

# ============ 新版 ============
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o", temperature=0.7)
model = init_chat_model("anthropic:claude-sonnet-4-20250514")
model = init_chat_model("groq:llama-3.3-70b-versatile")
```

#### EnsembleRetriever 迁移

```python
# ============ 旧版 ============
from langchain.retrievers import EnsembleRetriever
# 或
from langchain_community.retrievers import EnsembleRetriever

# ============ 新版 ============
from langchain_classic.retrievers import EnsembleRetriever
```

#### 消息格式迁移

```python
# ============ 旧版 ============
from langchain_core.messages import HumanMessage
msg = HumanMessage(content="你好")

# ============ 新版（兼容旧版，同时支持字典格式） ============
from langchain_core.messages import HumanMessage
msg = HumanMessage(content="你好")  # 仍然有效

# 新增：字典格式
msg = {"role": "user", "content": "你好"}  # 1.0 新增支持

# 在 agent.invoke 中两者都可以使用
agent.invoke({"messages": [HumanMessage(content="你好")]})
agent.invoke({"messages": [{"role": "user", "content": "你好"}]})
```

### 迁移检查清单

- [ ] 将所有 `create_react_agent` 替换为 `create_agent`
- [ ] 更新导入路径（`langgraph.prebuilt` -> `langchain.agents`）
- [ ] 使用 `init_chat_model()` 替代各厂商的 Chat Model 类
- [ ] 将 `EnsembleRetriever` 的导入改为 `langchain_classic`
- [ ] 测试所有 Agent 交互路径
- [ ] 验证工具调用是否正常工作
- [ ] 检查检查点兼容性

---

## 性能优化建议

### 1. 选择合适的模型

```python
# 场景化模型选择建议
MODEL_RECOMMENDATIONS = {
    "简单问答": "groq:llama-3.1-8b-instant",      # 快速、低成本
    "复杂推理": "groq:llama-3.3-70b-versatile",    # 强大、平衡
    "代码生成": "groq:llama-3.3-70b-versatile",    # 代码能力强
    "创意写作": "openai:gpt-4o",                    # 创造性好
    "结构化输出": "groq:llama-3.3-70b-versatile",   # 遵循格式好
    "嵌入计算": "all-MiniLM-L6-v2",                 # 本地、快速
}
```

### 2. 上下文管理策略

```python
# 策略一：滑动窗口
def sliding_window(messages: list, max_messages: int = 10) -> list:
    """保留最近 N 条消息"""
    if len(messages) <= max_messages:
        return messages
    # 保留第一条（系统消息）+ 最近 N-1 条
    return [messages[0]] + messages[-(max_messages-1):]

# 策略二：摘要压缩
async def compress_history(llm, messages: list) -> list:
    """将旧消息压缩为摘要"""
    if len(messages) <= 10:
        return messages

    old_messages = messages[1:-5]  # 保留首尾
    summary_prompt = "请简要总结以下对话内容：" + str(old_messages)
    summary = await llm.ainvoke(summary_prompt)

    return [
        messages[0],  # 系统消息
        {"role": "system", "content": f"之前的对话摘要：{summary.content}"},
    ] + messages[-5:]  # 最近 5 条

# 策略三：相关性过滤
def filter_by_relevance(messages: list, current_topic: str) -> list:
    """根据相关性过滤历史消息"""
    # 简单实现：只保留主题相关的消息
    relevant = [msg for msg in messages if current_topic in str(msg.content)]
    return relevant[-10:]  # 最多 10 条
```

### 3. 缓存策略

```python
# LLM 响应缓存
from langchain_core.globals import set_llm_cache
from langchain_community.cache import InMemoryCache

# 内存缓存（开发环境）
set_llm_cache(InMemoryCache())

# SQLite 缓存（生产环境）
from langchain_community.cache import SQLiteCache
set_llm_cache(SQLiteCache(database_path=".langchain.db"))

# 检索结果缓存
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_retrieve(query: str):
    """缓存检索结果"""
    return retriever.invoke(query)
```

### 4. 并发处理

```python
import asyncio

async def batch_process(questions: list[str]) -> list:
    """批量并发处理多个问题"""
    tasks = []
    for question in questions:
        task = agent.ainvoke({
            "messages": [{"role": "user", "content": question}],
        })
        tasks.append(task)

    # 并发执行，最多 5 个并发
    semaphore = asyncio.Semaphore(5)

    async def limited_task(task):
        async with semaphore:
            return await task

    results = await asyncio.gather(*[limited_task(t) for t in tasks])
    return results
```

### 5. 流式输出

```python
# 流式输出减少首字延迟
async def stream_response(agent, user_input: str):
    """流式输出 Agent 回答"""
    async for event in agent.astream({
        "messages": [{"role": "user", "content": user_input}],
    }):
        # 处理不同类型的事件
        if "messages" in event:
            for msg in event["messages"]:
                if hasattr(msg, "content") and msg.content:
                    print(msg.content, end="", flush=True)
```

---

## 学习资源

### 官方文档

| 资源 | 链接 | 说明 |
|------|------|------|
| LangChain 文档 | https://python.langchain.com/ | 核心框架文档 |
| LangGraph 文档 | https://langchain-ai.github.io/langgraph/ | 状态图框架文档 |
| LangChain API 参考 | https://api.python.langchain.com/ | API 详细参考 |
| LangGraph API 参考 | https://api.python.langchain.com/en/latest/langgraph/ | LangGraph API |
| Groq 文档 | https://console.groq.com/docs/ | Groq 模型文档 |

### 社区资源

| 资源 | 链接 | 说明 |
|------|------|------|
| LangChain GitHub | https://github.com/langchain-ai/langchain | 源码和 Issues |
| LangGraph GitHub | https://github.com/langchain-ai/langgraph | LangGraph 源码 |
| LangChain Hub | https://smith.langchain.com/hub | 提示词和 Agent 分享 |
| Discord 社区 | https://discord.gg/langchain | 官方 Discord |

### 推荐学习路径

```
阶段一：基础入门（1-2 周）
├── LLM 调用与提示词
├── 消息类型与对话管理
├── 工具定义与调用
└── 简单 Agent 构建

阶段二：实践应用（2-3 周）
├── 记忆与上下文管理
├── RAG 系统构建
├── 结构化输出
└── 多轮对话系统

阶段三：高级进阶（2-3 周）
├── LangGraph 状态图
├── 多 Agent 系统
├── 自定义中间件
└── 错误处理与重试

阶段四：项目实战（3-4 周）
├── 生产级 RAG 系统
├── 多 Agent 客服系统
├── 研究助手工作流
└── 部署与监控
```

### 推荐书籍与课程

1. **LangChain 官方教程**：最权威的学习资料，覆盖所有核心概念
2. **DeepLearning.AI LangChain 系列课程**：Andrew Ng 团队出品，免费
3. **《Building LLM Applications》**：系统性介绍 LLM 应用开发
4. **LangChain Cookbook**：官方实战案例集

---

## 附录：常用代码片段

### 快速启动模板

```python
"""LangChain 1.0 快速启动模板"""

import asyncio
from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage


@tool
def hello_tool(name: str) -> str:
    """向用户打招呼。

    Args:
        name: 用户的名字
    """
    return f"你好，{name}！欢迎使用 LangChain 1.0！"


async def main():
    # 初始化模型
    model = init_chat_model("groq:llama-3.3-70b-versatile")

    # 创建 Agent
    agent = create_agent(
        model=model,
        tools=[hello_tool],
        system_prompt="你是一个友好的助手，会使用工具和用户打招呼。",
    )

    # 运行
    result = await agent.ainvoke({
        "messages": [HumanMessage(content="我叫张三，请跟我打招呼")],
    })

    print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
```

### 调试工具

```python
"""调试辅助工具"""

def print_messages(result: dict):
    """打印完整消息历史"""
    for msg in result.get("messages", []):
        role = msg.__class__.__name__.replace("Message", "")
        content = msg.content[:200] if msg.content else "(空)"
        print(f"[{role}] {content}")

        # 打印工具调用
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"  -> 调用工具: {tc['name']}({tc['args']})")

        # 打印元数据
        if hasattr(msg, "response_metadata") and msg.response_metadata:
            model = msg.response_metadata.get("model_name", "未知")
            tokens = msg.response_metadata.get("token_usage", {})
            print(f"  模型: {model}, tokens: {tokens}")


def measure_latency(func):
    """测量函数执行时间的装饰器"""
    import time

    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[耗时] {func.__name__}: {elapsed:.2f}秒")
        return result

    return wrapper
```

---

> **上一章**：[26 - 项目实战：研究助手](./26-项目实战-研究助手.md)
