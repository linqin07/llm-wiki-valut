# LangChain 1.0 & LangGraph 1.0 完整知识体系

> 本知识库共 **29 个章节**，约 **29,000+ 行**，覆盖从入门到实战的全部知识点。

---

## 目录总览

### 第一阶段：基础篇（Modules 01-06）

| 章节 | 文件 | 主要内容 |
|------|------|---------|
| 00 | [概述与环境搭建](./00-概述与环境搭建.md) | LangChain/LangGraph 介绍、架构图、环境配置、Hello World |
| 01 | [LLM 基础与模型调用](./01-LLM基础与模型调用.md) | init_chat_model、三种输入格式、模型参数、响应结构 |
| 02 | [提示词模板](./02-提示词模板.md) | PromptTemplate、ChatPromptTemplate、LCEL 管道语法 |
| 03 | [消息系统与对话历史](./03-消息系统与对话历史.md) | 消息类型、对话历史管理、滑动窗口策略 |
| 04 | [自定义工具](./04-自定义工具.md) | @tool 装饰器、bind_tools、共享工具模块 |
| 05 | [Agent 基础](./05-Agent基础.md) | create_agent API、四层架构、三种视角、五大挑战 |
| 06 | [Agent 循环与流式输出](./06-Agent循环与流式输出.md) | ReAct 模式、.stream() 流式输出、中间状态检查 |

### 第二阶段：实用篇（Modules 07-15）

| 章节 | 文件 | 主要内容 |
|------|------|---------|
| 07 | [记忆系统](./07-记忆系统.md) | InMemorySaver、thread_id 会话管理、自动保存历史 |
| 08 | [上下文管理](./08-上下文管理.md) | SummarizationMiddleware、trim_messages、策略对比 |
| 09 | [持久化检查点](./09-持久化检查点.md) | SqliteSaver、跨进程验证、多用户会话 |
| 10 | [中间件系统](./10-中间件系统.md) | AgentMiddleware、洋葱模型、自定义中间件 |
| 11 | [结构化输出](./11-结构化输出.md) | Pydantic BaseModel、with_structured_output、Enum |
| 12 | [验证与重试](./12-验证与重试.md) | with_retry、with_fallbacks、field_validator |
| 13 | [RAG 基础](./13-RAG基础.md) | 文档加载、文本分块、嵌入、向量存储、相似度搜索 |
| 14 | [RAG 进阶](./14-RAG进阶.md) | BM25、混合搜索、EnsembleRetriever、RRF 算法 |
| 15 | [高级工具与 Agent 模式](./15-高级工具与Agent模式.md) | args_schema、异步工具、CallbackHandler、生产级配置 |

### 第三阶段：高级篇（Modules 16-23）

| 章节 | 文件 | 主要内容 |
|------|------|---------|
| 16 | [LangGraph 基础](./16-LangGraph基础.md) | StateGraph、节点、边、图编译执行 |
| 17 | [多 Agent 协作](./17-多Agent协作.md) | Supervisor/Collaborative/Hierarchical 模式、实战案例 |
| 18 | [条件路由](./18-条件路由.md) | add_conditional_edges、循环控制、错误处理路由 |
| 19 | [图像输入](./19-图像输入.md) | 视觉模型、URL/Base64 图像输入、图像分析工具 |
| 20 | [文件处理](./20-文件处理.md) | 多格式加载器、DirectoryLoader、分块策略 |
| 21 | [混合模态](./21-混合模态.md) | 文本+图像+结构化数据的混合工作流 |
| 22 | [LangSmith 集成](./22-LangSmith集成.md) | Trace 追踪、@traceable、性能监控 |
| 23 | [错误处理](./23-错误处理.md) | 重试、降级、自定义错误处理、优雅降级模式 |

### 第四阶段：项目实战篇

| 章节 | 文件 | 主要内容 |
|------|------|---------|
| 24 | [项目：RAG 系统](./24-项目实战-RAG系统.md) | 完整 RAG 流水线、引用追踪、置信度评分 |
| 25 | [项目：多 Agent 客服](./25-项目实战-多Agent客服.md) | 意图分类、专业 Agent、自动路由、质量检查 |
| 26 | [项目：研究助手](./26-项目实战-研究助手.md) | 多阶段研究工作流、多格式报告生成 |

### 补充章节

| 章节 | 文件 | 主要内容 |
|------|------|---------|
| 27 | [API 参考与常见问题](./27-API参考与常见问题.md) | API 速查表、常见错误、迁移指南、性能优化 |
| 28 | [意图识别系统](./28-意图识别系统.md) | 规则/ML/BERT 三种方法、槽位提取、多意图识别 |

---

## 学习路线建议

### 快速入门（1-2 周）
00 → 01 → 02 → 04 → 05 → 06 → 07

### 系统学习（3-4 周）
按顺序学习 00-15，配合代码实践

### 进阶深入（5-6 周）
16-23 + 28，结合项目实战 24-26

### 查漏补缺
27（API 参考与常见问题）随时查阅

---

## 核心 API 速查

```python
# 模型初始化
from langchain.chat_models import init_chat_model
model = init_chat_model("groq:llama-3.3-70b-versatile")

# Agent 创建（LangChain 1.0）
from langchain.agents import create_agent
agent = create_agent(model=model, tools=[...], system_prompt="...")

# 状态图（LangGraph）
from langgraph.graph import StateGraph, START, END

# 检查点
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

# 结构化输出
from pydantic import BaseModel
structured = model.with_structured_output(MyModel)

# 工具定义
from langchain_core.tools import tool
@tool
def my_func(param: str) -> str:
    """工具描述"""
    return "result"
```

---

*本知识库基于 LangChain 1.0 & LangGraph 1.0，参考了《大模型AI Agent知识从0-1笔记》等资料。*
