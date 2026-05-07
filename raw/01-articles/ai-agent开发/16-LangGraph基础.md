# 16 - LangGraph 基础

## 目录

- [LangGraph 是什么](#langgraph-是什么)
- [为什么需要 LangGraph](#为什么需要-langgraph)
- [StateGraph 核心概念](#stategraph-核心概念)
- [节点（Nodes）详解](#节点nodes详解)
- [边（Edges）详解](#边edges详解)
- [add_messages 注解](#add_messages-注解)
- [图的编译与执行](#图的编译与执行)
- [执行流程图](#执行流程图)
- [与 create_agent 的对比](#与-create_agent-的对比)
- [完整代码示例](#完整代码示例)
- [常见错误](#常见错误)
- [最佳实践](#最佳实践)
- [练习题](#练习题)

---

## LangGraph 是什么

LangGraph 是 LangChain 生态中的**有状态工作流框架**，它允许你用**图（Graph）**的方式构建复杂的 AI 应用。

```
传统链式调用（线性）:
  输入 -> 步骤A -> 步骤B -> 步骤C -> 输出

LangGraph（图结构）:
              +-------+
              | 开始   |
              +---+---+
                  |
           +------v------+
           |   节点 A     |
           +------+------+
                  |
        +---------v---------+
        |   条件判断         |
        +----+----------+---+
             |          |
       +-----v---+  +---v-----+
       | 节点 B  |  | 节点 C  |
       +----+----+  +----+----+
            |            |
            +-----+------+
                  |
           +------v------+
           |    结束      |
           +-------------+
```

**核心特点：**

| 特性 | 说明 |
|------|------|
| 基于图结构 | 节点（Node）和边（Edge）构成工作流 |
| 有状态 | 状态在整个图中流转，节点可以读取和修改 |
| 支持条件路由 | 运行时动态决定执行路径 |
| 支持循环 | 可以实现重试、迭代等循环逻辑 |
| 可持久化 | 通过 Checkpoint 保存和恢复状态 |
| 流式输出 | 支持逐节点或逐 token 的流式输出 |

---

## 为什么需要 LangGraph

### 线性链的局限性

LangChain 的 LCEL（LangChain Expression Language）适合简单的线性流程：

```python
# 线性链：简单但缺乏灵活性
chain = prompt | llm | parser
result = chain.invoke({"input": "你好"})
```

但实际的 Agent 应用需要更复杂的控制流：

```
用户提问 -> LLM 思考 -> 需要工具吗？
                          |
                    +-----+-----+
                    |           |
                   是          否
                    |           |
              调用工具      直接回复
                    |
              将结果返回 LLM
                    |
              需要继续吗？---是---+
                    |           |
                   否          回到思考
                    |
                  最终回复
```

### LangGraph 解决的问题

1. **条件分支**：根据运行时状态决定下一步
2. **循环执行**：Agent 可以多轮思考和调用工具
3. **状态管理**：在多个节点间共享和维护状态
4. **人机交互**：可以在特定节点暂停等待人工输入
5. **可观测性**：清晰的执行路径，便于调试

---

## StateGraph 核心概念

### TypedDict 定义状态模式

StateGraph 的核心是**状态（State）**。状态是一个 TypedDict，定义了图中所有节点共享的数据结构。

```python
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage

# 定义状态类型
class AgentState(TypedDict):
    """Agent 的状态定义"""
    messages: Annotated[list[BaseMessage], add_messages]
    # messages: 图中流转的消息列表
    # Annotated + add_messages: 新消息会追加而不是替换
```

### 创建 StateGraph

```python
from langgraph.graph import StateGraph

# 用状态类型初始化图
graph = StateGraph(AgentState)
```

**状态是整个图的数据中心：**

```
+------------------------------------------+
|              AgentState                   |
|                                           |
|  messages: [msg1, msg2, msg3, ...]       |
|  custom_field: "some value"              |
|  step_count: 3                           |
+------------------------------------------+
        ^               ^               ^
        |               |               |
   读取+写入       读取+写入        读取+写入
        |               |               |
   +----+----+    +-----+----+    +-----+----+
   | 节点 A  |    |  节点 B  |    |  节点 C  |
   +---------+    +----------+    +----------+
```

### 状态设计示例

```python
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class ResearchState(TypedDict):
    """研究助手的状态"""
    # 消息历史
    messages: Annotated[list[BaseMessage], add_messages]
    # 研究主题
    topic: str
    # 调研结果
    research_results: list[str]
    # 最终报告
    report: str
    # 当前步骤
    current_step: str
```

---

## 节点（Nodes）详解

### 节点是普通 Python 函数

节点是图中的处理单元，本质上就是一个 Python 函数。

**节点函数签名：**
- **输入**：当前状态（TypedDict）
- **输出**：状态更新（字典，部分更新）

```python
def my_node(state: AgentState) -> dict:
    """一个简单的节点函数"""
    # 读取状态
    messages = state["messages"]

    # 执行逻辑
    response = llm.invoke(messages)

    # 返回状态更新（部分更新，不是全量替换）
    return {"messages": [response]}
```

### 节点命名

```python
# 方式1：使用函数名作为节点名
graph.add_node(my_node)  # 节点名 = "my_node"

# 方式2：显式指定节点名
graph.add_node("custom_name", my_node)
```

### 节点命名规则

```python
# 推荐：使用有意义的名称
graph.add_node("researcher", research_node)
graph.add_node("writer", writer_node)
graph.add_node("editor", editor_node)

# 不推荐：使用无意义的名称
graph.add_node("step1", func_a)
graph.add_node("step2", func_b)
```

### 节点内调用 LLM

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("groq:llama-3.3-70b-versatile")

def llm_node(state: AgentState) -> dict:
    """调用 LLM 的节点"""
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}
```

### 节点内调用工具

```python
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"搜索结果: {query}"

def tool_node(state: AgentState) -> dict:
    """调用工具的节点"""
    last_message = state["messages"][-1]
    # 解析工具调用
    tool_calls = last_message.tool_calls
    results = []
    for tc in tool_calls:
        if tc["name"] == "search":
            result = search.invoke(tc["args"])
            results.append(result)
    return {"messages": results}
```

---

## 边（Edges）详解

### 静态边

静态边定义了固定的节点连接关系：

```python
from langgraph.graph import StateGraph, START, END

graph = StateGraph(AgentState)

# 添加节点
graph.add_node("greet", greet_node)
graph.add_node("process", process_node)
graph.add_node("output", output_node)

# 添加静态边（固定路径）
graph.add_edge(START, "greet")       # 从起点到 greet
graph.add_edge("greet", "process")   # 从 greet 到 process
graph.add_edge("process", "output")  # 从 process 到 output
graph.add_edge("output", END)        # 从 output 到终点
```

**静态边的流程图：**

```
START --> greet --> process --> output --> END
```

### START 和 END 常量

```python
from langgraph.graph import START, END

# START: 图的入口点，虚拟起始节点
# END:   图的出口点，虚拟终止节点

# 每个图都必须有从 START 出发的边
# 每个图都应该有到达 END 的边（否则图会无限执行）
```

### 条件边（简介）

条件边根据运行时状态动态决定下一个节点：

```python
# 条件边：根据状态决定下一步
graph.add_conditional_edges(
    "decision_node",           # 源节点
    condition_function,        # 条件函数
    {
        "option_a": "node_a",  # 条件值 -> 目标节点
        "option_b": "node_b",
    }
)
```

> **注意**：条件路由的详细内容请参见 [第18章-条件路由](./18-条件路由.md)。

---

## add_messages 注解

### 问题：列表的默认行为

在 TypedDict 中，如果一个字段是 `list` 类型，当你返回一个新列表时，它会**替换**原来的列表：

```python
# 问题示例
class BadState(TypedDict):
    messages: list  # 没有 add_messages 注解

# 初始状态: {"messages": [msg1, msg2]}
# 节点返回: {"messages": [msg3]}
# 最终状态: {"messages": [msg3]}  ← msg1, msg2 丢失了！
```

### 解决方案：add_messages

```python
from typing import Annotated
from langgraph.graph.message import add_messages

class GoodState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# 初始状态: {"messages": [msg1, msg2]}
# 节点返回: {"messages": [msg3]}
# 最终状态: {"messages": [msg1, msg2, msg3]}  ← 正确追加！
```

### add_messages 的工作原理

```
状态中的 messages:    [msg1, msg2]
节点返回的 messages:  [msg3, msg4]
                           |
                      add_messages 合并
                           |
                           v
最终 messages:        [msg1, msg2, msg3, msg4]
```

### 自定义合并函数

```python
from operator import add
from typing import Annotated

def merge_lists(existing: list, new: list) -> list:
    """自定义合并逻辑：去重后追加"""
    combined = existing + new
    # 简单去重
    seen = set()
    result = []
    for item in combined:
        key = str(item)
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result

class CustomState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    tags: Annotated[list[str], merge_lists]  # 自定义合并
```

---

## 图的编译与执行

### 编译图

```python
# 编译图，生成可执行的应用
app = graph.compile()

# 带 Checkpointer 的编译（支持状态持久化）
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
app = graph.compile(checkpointer=memory)
```

### 执行图

```python
# 基本执行
result = app.invoke({
    "messages": [{"role": "user", "content": "你好"}]
})

# 带配置的执行（需要 checkpointer 时）
config = {"configurable": {"thread_id": "session-1"}}
result = app.invoke(
    {"messages": [{"role": "user", "content": "你好"}]},
    config=config
)
```

### 流式执行

```python
# 方式1：按节点流式输出
for event in app.stream(input_data, config):
    for node_name, node_output in event.items():
        print(f"节点 {node_name} 输出: {node_output}")

# 方式2：按 token 流式输出
for token, metadata in app.stream(input_data, stream_mode="messages"):
    print(token, end="")
```

---

## 执行流程图

### 完整的图执行流程

```
用户输入
    |
    v
+---+---+
| START |
+---+---+
    |
    v
+-------+-------+
|  初始化节点    |  ← 设置初始状态
+-------+-------+
    |
    v
+-------+-------+
|   处理节点 A   |  ← 执行主要逻辑
+-------+-------+
    |
    v
+-------+-------+
|   条件判断     |  ← 根据状态决定路径
+---+-------+---+
    |       |
    v       v
+---+---+ +---+---+
| 节点B | | 节点C |  ← 不同的处理路径
+---+---+ +---+---+
    |       |
    +---+---+
        |
        v
+-------+-------+
|   输出节点     |  ← 格式化输出
+-------+-------+
    |
    v
+---+---+
|  END  |
+---+---+
    |
    v
返回结果给用户
```

### 状态流转示意

```
步骤1 (START->init):
  状态: {messages: [user_msg]}

步骤2 (init->process):
  状态: {messages: [user_msg], initialized: true}

步骤3 (process->decision):
  状态: {messages: [user_msg, ai_msg], need_tool: true}

步骤4 (decision->tool_node):
  状态: {messages: [user_msg, ai_msg, tool_call], need_tool: true}

步骤5 (tool_node->process):
  状态: {messages: [user_msg, ai_msg, tool_call, tool_result], need_tool: false}

步骤6 (process->output):
  状态: {messages: [...全部消息], final_answer: "..."}
```

---

## 与 create_agent 的对比

### create_agent 内部实现

`create_agent` 是 LangChain 提供的高级 API，其内部就是构建了一个 StateGraph：

```python
from langchain.agents import create_agent

# 使用 create_agent（高级 API）
agent = create_agent(
    model=model,
    tools=[search, calculate],
    system_prompt="你是一个助手"
)
response = agent.invoke({"messages": [{"role": "user", "content": "你好"}]})
```

### create_agent 内部的图结构

```
create_agent 内部大致等价于：

graph = StateGraph(AgentState)
graph.add_node("llm", call_model)
graph.add_node("tools", tool_executor)
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_continue, {
    "continue": "tools",
    "end": END,
})
graph.add_edge("tools", "llm")
app = graph.compile()
```

### 对比表

| 方面 | create_agent | 手动构建 StateGraph |
|------|-------------|-------------------|
| 复杂度 | 简单，一行代码 | 需要手动定义每个部分 |
| 灵活性 | 有限，标准 Agent 模式 | 完全自定义 |
| 适用场景 | 标准工具调用 Agent | 复杂工作流、多 Agent |
| 状态管理 | 自动处理 | 手动定义状态类型 |
| 节点逻辑 | 固定（LLM + 工具） | 任意 Python 函数 |
| 条件路由 | 自动（工具调用判断） | 手动定义条件函数 |

### 何时使用哪个

```python
# 使用 create_agent：标准的工具调用 Agent
agent = create_agent(model=model, tools=[...], system_prompt="...")

# 使用 StateGraph：需要自定义控制流时
graph = StateGraph(MyState)
# ... 自定义节点和边
```

---

## 完整代码示例

### 示例1：简单的问候图

```python
"""
LangGraph 基础示例：简单的问候图
演示 StateGraph 的基本用法
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# 第一步：定义状态
class GreetState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    greeting: str

# 第二步：定义节点函数
def greet_node(state: GreetState) -> dict:
    """问候节点：生成问候语"""
    last_msg = state["messages"][-1].content
    if "早上" in last_msg:
        greeting = "早上好！祝你今天愉快！"
    elif "晚上" in last_msg:
        greeting = "晚上好！辛苦了一天！"
    else:
        greeting = "你好！很高兴见到你！"
    return {
        "messages": [AIMessage(content=greeting)],
        "greeting": greeting,
    }

def format_node(state: GreetState) -> dict:
    """格式化节点：添加格式"""
    formatted = f"=== {state['greeting']} ==="
    return {"messages": [AIMessage(content=formatted)]}

# 第三步：构建图
graph = StateGraph(GreetState)
graph.add_node("greet", greet_node)
graph.add_node("format", format_node)

# 第四步：添加边
graph.add_edge(START, "greet")
graph.add_edge("greet", "format")
graph.add_edge("format", END)

# 第五步：编译并执行
app = graph.compile()
result = app.invoke({
    "messages": [HumanMessage(content="早上好！")]
})
print(result["messages"][-1].content)
# 输出: === 早上好！祝你今天愉快！ ===
```

### 示例2：带 LLM 的处理图

```python
"""
LangGraph 进阶示例：带 LLM 的处理图
演示如何在节点中调用 LLM
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

# 初始化模型
model = init_chat_model("groq:llama-3.3-70b-versatile")

# 定义状态
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    summary: str

# 定义节点
def chat_node(state: ChatState) -> dict:
    """对话节点：调用 LLM 生成回复"""
    system_msg = SystemMessage(content="你是一个友好的助手，请简洁地回答问题。")
    messages = [system_msg] + state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def summarize_node(state: ChatState) -> dict:
    """总结节点：总结对话内容"""
    summary_prompt = [
        SystemMessage(content="请用一句话总结以下对话。"),
        *state["messages"]
    ]
    response = model.invoke(summary_prompt)
    return {"summary": response.content}

# 构建图
graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)
graph.add_node("summarize", summarize_node)

graph.add_edge(START, "chat")
graph.add_edge("chat", "summarize")
graph.add_edge("summarize", END)

# 编译并执行
app = graph.compile()
result = app.invoke({
    "messages": [HumanMessage(content="什么是 LangGraph？")]
})

print("回复:", result["messages"][-1].content)
print("总结:", result["summary"])
```

---

## 常见错误

### 1. 忘记添加 add_messages 注解

```python
# 错误：消息会被替换而不是追加
class BadState(TypedDict):
    messages: list[BaseMessage]

# 正确：使用 add_messages 注解
class GoodState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

### 2. 节点返回了完整状态而非更新

```python
# 错误：返回了完整的状态
def bad_node(state: AgentState) -> dict:
    return {
        "messages": state["messages"] + [new_msg],  # 全量
        "other_field": state["other_field"],         # 重复
    }

# 正确：只返回变更的部分
def good_node(state: AgentState) -> dict:
    return {"messages": [new_msg]}  # 只返回新增的消息
```

### 3. 忘记连接 START 或 END

```python
# 错误：没有从 START 出发的边
graph = StateGraph(AgentState)
graph.add_node("process", process_node)
graph.add_edge("process", END)
app = graph.compile()  # 报错！没有入口

# 正确：必须有 START -> 某个节点
graph.add_edge(START, "process")
graph.add_edge("process", END)
```

### 4. 节点名称不匹配

```python
# 错误：边引用了不存在的节点
graph.add_node("greet", greet_func)
graph.add_edge(START, "greting")  # 拼写错误！

# 正确：确保节点名完全匹配
graph.add_edge(START, "greet")
```

---

## 最佳实践

### 1. 状态设计要简洁

```python
# 好的设计：只包含必要的字段
class CleanState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    context: str

# 不好的设计：冗余字段太多
class MessyState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    raw_input: str           # 冗余，messages 里已有
    processed_input: str     # 冗余
    temp_data: dict          # 临时数据不应在状态中
    debug_info: str          # 调试信息不应在状态中
```

### 2. 节点职责单一

```python
# 好：每个节点只做一件事
def fetch_data(state):
    """只负责获取数据"""
    data = api_call(state["query"])
    return {"data": data}

def process_data(state):
    """只负责处理数据"""
    result = transform(state["data"])
    return {"result": result}

# 不好：一个节点做了太多事
def do_everything(state):
    """获取、处理、输出全在一起"""
    data = api_call(state["query"])
    result = transform(data)
    output = format(result)
    return {"output": output}
```

### 3. 使用有意义的节点名

```python
# 好：名称反映功能
graph.add_node("fetch_research", fetch_node)
graph.add_node("analyze_results", analyze_node)
graph.add_node("generate_report", report_node)

# 不好：名称无意义
graph.add_node("step1", fetch_node)
graph.add_node("step2", analyze_node)
graph.add_node("step3", report_node)
```

### 4. 错误处理要完善

```python
def safe_node(state: AgentState) -> dict:
    """带错误处理的节点"""
    try:
        result = risky_operation(state)
        return {"result": result}
    except Exception as e:
        return {"error": str(e), "messages": [AIMessage(content=f"出错了: {e}")]}
```

---

## 练习题

### 练习1：基础图构建

构建一个简单的三步处理图：
1. **输入节点**：接收用户输入并存储到状态
2. **处理节点**：将输入转为大写
3. **输出节点**：格式化输出

```python
# 在此编写你的代码
# 提示：
# 1. 定义 TypedDict 状态
# 2. 编写三个节点函数
# 3. 构建图并添加边
# 4. 编译并执行
```

### 练习2：带 LLM 的问答图

构建一个问答图：
1. **分类节点**：判断用户问题是关于天气还是数学
2. **天气节点**：回答天气相关问题
3. **数学节点**：回答数学相关问题
4. **总结节点**：总结回答

```python
# 在此编写你的代码
# 提示：分类节点需要返回类别信息到状态中
```

### 练习3：多轮对话图

构建一个支持多轮对话的图：
1. 使用 MemorySaver 进行状态持久化
2. 对话节点调用 LLM
3. 检查节点判断是否需要继续对话
4. 支持通过 thread_id 维护多个独立会话

```python
# 在此编写你的代码
# 提示：
# 1. 使用 MemorySaver 作为 checkpointer
# 2. config 中设置 thread_id
# 3. 多次调用 app.invoke() 模拟多轮对话
```

---

**下一章**：[17-多Agent协作](./17-多Agent协作.md) - 学习如何构建多个 Agent 协作的系统
