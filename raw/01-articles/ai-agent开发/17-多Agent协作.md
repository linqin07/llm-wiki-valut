# 17 - 多 Agent 协作

## 目录

- [多 Agent 系统的必要性](#多-agent-系统的必要性)
- [三种协作模式详解](#三种协作模式详解)
- [Supervisor 模式（主管模式）](#supervisor-模式主管模式)
- [Collaborative 模式（协作模式）](#collaborative-模式协作模式)
- [Hierarchical 模式（层级模式）](#hierarchical-模式层级模式)
- [Send() 动态分派](#send-动态分派)
- [Agent 间共享状态](#agent-间共享状态)
- [实例：内容创作团队](#实例内容创作团队)
- [完整代码示例](#完整代码示例)
- [常见错误](#常见错误)
- [最佳实践](#最佳实践)
- [多 Agent 实战案例：智能软件开发团队](#多-agent-实战案例智能软件开发团队)
- [多 Agent 协作的三大挑战](#多-agent-协作的三大挑战)
- [多 Agent 通信模式对比](#多-agent-通信模式对比)
- [练习题](#练习题)

---

## 多 Agent 系统的必要性

### 单 Agent 的局限性

当任务复杂度增加时，单个 Agent 会面临以下问题：

```
单 Agent 尝试做所有事情：
+--------------------------------------------------+
|                    单个 Agent                      |
|                                                    |
|  需要调研？──> 调用搜索工具                        |
|  需要写作？──> 自己生成文本                        |
|  需要翻译？──> 自己翻译                            |
|  需要审核？──> 自己审核（但可能有偏见）            |
|                                                    |
|  问题：                                              |
|  1. system_prompt 越来越长，角色混乱               |
|  2. 工具太多，选择困难                              |
|  3. 上下文窗口容易超限                              |
|  4. 无法并行处理                                    |
+--------------------------------------------------+
```

### 多 Agent 的优势

```
多 Agent 分工协作：
+----------+     +----------+     +----------+
| Research | --> |  Writer  | --> |  Editor  |
|  Agent   |     |  Agent   |     |  Agent   |
+----------+     +----------+     +----------+
     |                |                |
  负责调研         负责写作         负责编辑
  搜索工具         写作工具         审核工具
  信息收集         内容生成         质量检查
```

| 对比维度 | 单 Agent | 多 Agent |
|---------|---------|---------|
| 角色清晰度 | 角色混乱 | 每个 Agent 专注一个角色 |
| 工具数量 | 工具过多 | 每个 Agent 只需少量工具 |
| 上下文利用 | 上下文冗长 | 按需传递相关信息 |
| 并行处理 | 串行执行 | 可并行执行独立任务 |
| 可维护性 | 难以维护 | 各 Agent 独立维护 |
| 可扩展性 | 难以扩展 | 添加新 Agent 即可扩展 |

---

## 三种协作模式详解

### 模式总览

```
1. Supervisor 模式（主管模式）:
   +------------+
   | Supervisor |
   +--+---+---+-+
      |   |   |
      v   v   v
   +--+ +--+ +--+
   |A | |B | |C |
   +--+ +--+ +--+

2. Collaborative 模式（协作模式）:
   +--+    +--+
   |A |<-->|B |
   +--+    +--+
    ^       ^
    |       |
    v       v
   +--+    +--+
   |C |<-->|D |
   +--+    +--+

3. Hierarchical 模式（层级模式）:
         +------+
         | Boss |
         +--+---+
            |
      +-----+-----+
      |           |
   +--+--+     +--+--+
   |Lead1|     |Lead2|
   +--+--+     +--+--+
      |           |
   +--+--+     +--+--+
   |Work |     |Work |
   |Team |     |Team |
   +-----+     +-----+
```

---

## Supervisor 模式（主管模式）

### 工作原理

Supervisor 模式是最常用的多 Agent 协作模式。中央协调器（Supervisor）负责：
1. 分析用户请求
2. 决定由哪个工作 Agent 处理
3. 将任务分派给对应 Agent
4. 收集结果并汇总

```
用户请求
    |
    v
+---+---+
|Super- |
|visor  |  <-- 决定由谁来处理
+---+---+
    |
    +---+---+---+
    |       |   |
    v       v   v
+------+ +------+ +------+
|Agent | |Agent | |Agent |
|  A   | |  B   | |  C   |
+--+---+ +--+---+ +--+---+
   |        |        |
   +---+----+--------+
       |
       v
  返回给 Supervisor
       |
       v
    最终回复
```

### 代码实现

```python
"""
Supervisor 模式示例
"""
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import init_chat_model

model = init_chat_model("groq:llama-3.3-70b-versatile")

# 定义状态
class SupervisorState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    next_agent: str  # Supervisor 决定的下一个 Agent

# Supervisor 节点：决定下一步
def supervisor_node(state: SupervisorState) -> dict:
    """Supervisor 分析请求，决定由哪个 Agent 处理"""
    system_prompt = SystemMessage(content="""你是一个任务协调员。
根据用户的问题，决定应该由哪个专家处理：
- "researcher": 需要调研、搜索信息时
- "writer": 需要写作、生成内容时
- "analyst": 需要数据分析时

只回复专家名称，不要回复其他内容。""")

    response = model.invoke([system_prompt] + state["messages"])

    # 解析 Supervisor 的决定
    agent_name = response.content.strip().lower()
    if agent_name not in ["researcher", "writer", "analyst"]:
        agent_name = "writer"  # 默认使用 writer

    return {
        "messages": [AIMessage(content=f"[Supervisor] 派发给 {agent_name}")],
        "next_agent": agent_name,
    }

# 工作 Agent 节点
def researcher_node(state: SupervisorState) -> dict:
    """调研专家"""
    prompt = SystemMessage(content="你是调研专家，擅长搜索和整理信息。")
    response = model.invoke([prompt] + state["messages"])
    return {"messages": [AIMessage(content=f"[Researcher] {response.content}")]}

def writer_node(state: SupervisorState) -> dict:
    """写作专家"""
    prompt = SystemMessage(content="你是写作专家，擅长生成高质量的文本内容。")
    response = model.invoke([prompt] + state["messages"])
    return {"messages": [AIMessage(content=f"[Writer] {response.content}")]}

def analyst_node(state: SupervisorState) -> dict:
    """分析专家"""
    prompt = SystemMessage(content="你是数据分析专家，擅长解读数据和趋势。")
    response = model.invoke([prompt] + state["messages"])
    return {"messages": [AIMessage(content=f"[Analyst] {response.content}")]}

# 路由函数
def route_to_agent(state: SupervisorState) -> str:
    """根据 Supervisor 的决定路由到对应 Agent"""
    return state["next_agent"]

# 构建图
graph = StateGraph(SupervisorState)

# 添加节点
graph.add_node("supervisor", supervisor_node)
graph.add_node("researcher", researcher_node)
graph.add_node("writer", writer_node)
graph.add_node("analyst", analyst_node)

# 添加边
graph.add_edge(START, "supervisor")
graph.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "researcher": "researcher",
        "writer": "writer",
        "analyst": "analyst",
    }
)
graph.add_edge("researcher", END)
graph.add_edge("writer", END)
graph.add_edge("analyst", END)

# 编译并执行
app = graph.compile()
result = app.invoke({
    "messages": [HumanMessage(content="帮我分析一下 AI 行业的发展趋势")]
})
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 控制流清晰，易于理解和调试 | Supervisor 是单点瓶颈 |
| 任务分配明确 | Supervisor 决策可能不准确 |
| 易于添加新的工作 Agent | 所有通信经过 Supervisor，效率较低 |
| 状态管理简单 | 不适合需要 Agent 间频繁交互的场景 |

---

## Collaborative 模式（协作模式）

### 工作原理

协作模式中，Agent 之间直接点对点通信，没有中央协调器。

```
+---------+      直接通信      +---------+
| Agent A | <─────────────────> | Agent B |
+---------+                    +---------+
    ^                              ^
    |                              |
    v                              v
+---------+      直接通信      +---------+
| Agent C | <─────────────────> | Agent D |
+---------+                    +---------+
```

### 代码实现

```python
"""
Collaborative 模式示例：两个 Agent 直接协作
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import init_chat_model

model = init_chat_model("groq:llama-3.3-70b-versatile")

class CollabState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    draft: str         # 草稿内容
    feedback: str      # 反馈内容
    iteration: int     # 迭代次数

def writer_agent(state: CollabState) -> dict:
    """写作 Agent：根据反馈生成或修改内容"""
    if state.get("feedback"):
        prompt = f"根据以下反馈修改你的草稿：\n{state['draft']}\n\n反馈：{state['feedback']}"
    else:
        prompt = "请写一篇关于 AI 发展的简短文章（100字以内）。"

    response = model.invoke([
        SystemMessage(content="你是写作专家。"),
        HumanMessage(content=prompt)
    ])

    return {
        "draft": response.content,
        "messages": [AIMessage(content=f"[Writer] 新草稿：{response.content}")],
        "iteration": state.get("iteration", 0) + 1,
    }

def reviewer_agent(state: CollabState) -> dict:
    """审阅 Agent：审阅草稿并给出反馈"""
    response = model.invoke([
        SystemMessage(content="你是文章审阅专家。请审阅以下文章并给出改进建议。如果文章质量很好，回复'APPROVED'。"),
        HumanMessage(content=state["draft"])
    ])

    return {
        "feedback": response.content,
        "messages": [AIMessage(content=f"[Reviewer] 反馈：{response.content}")],
    }

def should_continue(state: CollabState) -> str:
    """判断是否需要继续迭代"""
    # 最多迭代 3 次
    if state.get("iteration", 0) >= 3:
        return "end"
    # 如果审阅通过
    if "APPROVED" in state.get("feedback", "").upper():
        return "end"
    return "continue"

# 构建图
graph = StateGraph(CollabState)
graph.add_node("writer", writer_agent)
graph.add_node("reviewer", reviewer_agent)

graph.add_edge(START, "writer")
graph.add_edge("writer", "reviewer")
graph.add_conditional_edges(
    "reviewer",
    should_continue,
    {"continue": "writer", "end": END}
)

app = graph.compile()
result = app.invoke({
    "messages": [HumanMessage(content="写一篇关于 AI 的文章")],
    "draft": "",
    "feedback": "",
    "iteration": 0,
})
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 灵活，Agent 间直接通信 | 复杂度高，难以追踪流程 |
| 无单点瓶颈 | 状态管理复杂 |
| 适合需要频繁交互的场景 | 调试困难 |
| 可以实现复杂的协商逻辑 | 容易出现死循环 |

---

## Hierarchical 模式（层级模式）

### 工作原理

层级模式是 Supervisor 模式的扩展，形成树形结构的 Agent 团队。

```
              +-----------+
              | 顶层主管  |
              +-----+-----+
                    |
         +----------+----------+
         |                     |
   +-----+-----+        +-----+-----+
   | 团队主管A  |        | 团队主管B  |
   +-----+-----+        +-----+-----+
         |                     |
    +----+----+           +----+----+
    |         |           |         |
+---+--+ +---+--+   +---+--+ +---+--+
|Agent | |Agent |   |Agent | |Agent |
| A1   | | A2   |   | B1   | | B2   |
+------+ +------+   +------+ +------+
```

### 代码实现

```python
"""
Hierarchical 模式示例
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import init_chat_model

model = init_chat_model("groq:llama-3.3-70b-versatile")

class HierState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    task_type: str       # 任务类型
    team_results: dict   # 各团队结果
    final_result: str    # 最终结果

# 顶层主管
def top_supervisor(state: HierState) -> dict:
    """顶层主管：决定由哪个团队处理"""
    response = model.invoke([
        SystemMessage(content="你是总负责人。根据任务类型决定：'content' 团队或 'research' 团队。只回复团队名。"),
        *state["messages"]
    ])
    team = response.content.strip().lower()
    if team not in ["content", "research"]:
        team = "content"
    return {"task_type": team}

# 内容团队主管
def content_lead(state: HierState) -> dict:
    """内容团队主管"""
    response = model.invoke([
        SystemMessage(content="你是内容团队主管，协调写作和编辑任务。"),
        *state["messages"]
    ])
    return {"messages": [AIMessage(content=f"[Content Lead] {response.content}")]}

# 研究团队主管
def research_lead(state: HierState) -> dict:
    """研究团队主管"""
    response = model.invoke([
        SystemMessage(content="你是研究团队主管，协调调研和分析任务。"),
        *state["messages"]
    ])
    return {"messages": [AIMessage(content=f"[Research Lead] {response.content}")]}

# 路由函数
def route_to_team(state: HierState) -> str:
    return state["task_type"]

# 构建图
graph = StateGraph(HierState)
graph.add_node("top_supervisor", top_supervisor)
graph.add_node("content_lead", content_lead)
graph.add_node("research_lead", research_lead)

graph.add_edge(START, "top_supervisor")
graph.add_conditional_edges(
    "top_supervisor",
    route_to_team,
    {"content": "content_lead", "research": "research_lead"}
)
graph.add_edge("content_lead", END)
graph.add_edge("research_lead", END)

app = graph.compile()
```

### 优缺点

| 优点 | 缺点 |
|------|------|
| 可扩展，适合大型系统 | 层级多，延迟增加 |
| 团队自治，减少顶层负担 | 信息传递可能失真 |
| 符合组织管理结构 | 设计复杂度高 |

---

## Send() 动态分派

### 什么是 Send

`Send` 允许在运行时动态决定将任务发送给哪些 Agent，支持并行执行。

```python
from langgraph.types import Send

# Send 的签名
# Send(node_name: str, state_update: dict)
```

### 使用场景

```
用户请求："同时调研三个主题"
              |
              v
        +-----+-----+
        |  分派节点   |
        +-----+-----+
              |
    +---------+---------+
    |         |         |
    v         v         v
+---+---+ +---+---+ +---+---+
|调研主题A| |调研主题B| |调研主题C|  <-- 并行执行
+--------+ +--------+ +--------+
    |         |         |
    +---------+---------+
              |
              v
        +-----+-----+
        |  汇总节点   |
        +-----------+
```

### 代码示例

```python
"""
Send 动态分派示例
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

# 每个子任务的状态
class SubTaskState(TypedDict):
    topic: str
    messages: Annotated[list[BaseMessage], add_messages]

# 主图状态
class MainState(TypedDict):
    topics: list[str]
    results: Annotated[list[str], lambda x, y: x + y]  # 合并结果
    messages: Annotated[list[BaseMessage], add_messages]

# 子任务处理节点
def research_topic(state: SubTaskState) -> dict:
    """调研单个主题"""
    # 这里可以调用 LLM 或工具
    result = f"关于 '{state['topic']}' 的调研结果..."
    return {"messages": [AIMessage(content=result)]}

# 分派节点
def dispatch_tasks(state: MainState) -> list:
    """将每个主题分派给独立的调研节点"""
    return [
        Send("researcher", {"topic": topic, "messages": []})
        for topic in state["topics"]
    ]

# 汇总节点
def aggregate_results(state: MainState) -> dict:
    """汇总所有调研结果"""
    combined = "\n".join(state["results"])
    return {"messages": [AIMessage(content=f"汇总结果：\n{combined}")]}

# 构建图
graph = StateGraph(MainState)
graph.add_node("researcher", research_topic)
graph.add_node("aggregator", aggregate_results)

graph.add_edge(START, "aggregator")
# 使用 Send 动态分派
graph.add_conditional_edges(START, dispatch_tasks)
graph.add_edge("researcher", "aggregator")
graph.add_edge("aggregator", END)

app = graph.compile()
result = app.invoke({
    "topics": ["AI 发展趋势", "量子计算进展", "新能源技术"],
    "results": [],
    "messages": [],
})
```

---

## Agent 间共享状态

### 状态共享机制

在 LangGraph 中，所有节点共享同一个状态对象，这是 Agent 间通信的基础。

```
+---------------------------------------------------+
|                  共享状态 (State)                   |
|                                                    |
|  messages: [...]                                   |
|  research_data: {...}    <-- Researcher 写入       |
|  draft: "..."            <-- Writer 读取并写入     |
|  feedback: "..."         <-- Editor 读取并写入     |
+---------------------------------------------------+
        ^           ^           ^
        |           |           |
   +----+---+ +-----+----+ +---+----+
   |Research| |  Writer  | | Editor |
   | Agent  | |  Agent   | | Agent  |
   +--------+ +----------+ +--------+
```

### 设计共享状态

```python
class SharedState(TypedDict):
    # 消息历史（所有 Agent 可见）
    messages: Annotated[list[BaseMessage], add_messages]

    # 研究数据（Researcher 写入，Writer 读取）
    research_data: dict

    # 草稿（Writer 写入，Editor 读取）
    draft: str

    # 审核结果（Editor 写入）
    review_result: str

    # 控制信息
    current_phase: str  # "research" | "writing" | "editing"
```

---

## 实例：内容创作团队

### 系统设计

```
用户: "写一篇关于 AI 的博客文章"
         |
         v
+--------+--------+
|   Supervisor     |
|   (协调者)       |
+--------+--------+
         |
    +----+----+
    |         |
    v         v
+---+---+ +---+---+
|Research| | Writer|
| Agent  | | Agent |
+---+---+ +---+---+
    |         |
    v         v
+---+---+
| Editor |
| Agent  |
+---+---+
    |
    v
  最终输出
```

### 完整实现

```python
"""
内容创作团队 - 完整的多 Agent 协作示例
"""
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import init_chat_model

model = init_chat_model("groq:llama-3.3-70b-versatile")

# ---- 状态定义 ----
class TeamState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    topic: str
    research: str
    draft: str
    final_article: str
    next_agent: str

# ---- Agent 节点 ----
def supervisor(state: TeamState) -> dict:
    """主管：协调整个创作流程"""
    if not state.get("research"):
        next_agent = "researcher"
    elif not state.get("draft"):
        next_agent = "writer"
    elif not state.get("final_article"):
        next_agent = "editor"
    else:
        next_agent = "end"

    return {
        "next_agent": next_agent,
        "messages": [AIMessage(content=f"[Supervisor] 当前阶段: {next_agent}")]
    }

def researcher(state: TeamState) -> dict:
    """调研员：收集和整理信息"""
    response = model.invoke([
        SystemMessage(content="你是调研专家。请为以下主题收集关键信息和要点，输出结构化的调研结果。"),
        HumanMessage(content=f"主题：{state['topic']}")
    ])
    return {
        "research": response.content,
        "messages": [AIMessage(content=f"[Researcher] 调研完成")]
    }

def writer(state: TeamState) -> dict:
    """写手：根据调研结果撰写文章"""
    response = model.invoke([
        SystemMessage(content="你是专业写手。根据调研资料撰写一篇博客文章。文章应结构清晰、内容丰富。"),
        HumanMessage(content=f"调研资料：\n{state['research']}\n\n主题：{state['topic']}")
    ])
    return {
        "draft": response.content,
        "messages": [AIMessage(content=f"[Writer] 初稿完成")]
    }

def editor(state: TeamState) -> dict:
    """编辑：审阅和优化文章"""
    response = model.invoke([
        SystemMessage(content="""你是资深编辑。请审阅文章并：
1. 修正语法和拼写错误
2. 优化文章结构
3. 增强可读性
4. 输出最终版本"""),
        HumanMessage(content=f"待审阅文章：\n{state['draft']}")
    ])
    return {
        "final_article": response.content,
        "messages": [AIMessage(content=f"[Editor] 编辑完成")]
    }

# ---- 路由函数 ----
def route_next(state: TeamState) -> str:
    return state["next_agent"]

# ---- 构建图 ----
graph = StateGraph(TeamState)

graph.add_node("supervisor", supervisor)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.add_node("editor", editor)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges(
    "supervisor",
    route_next,
    {
        "researcher": "researcher",
        "writer": "writer",
        "editor": "editor",
        "end": END,
    }
)
graph.add_edge("researcher", "supervisor")
graph.add_edge("writer", "supervisor")
graph.add_edge("editor", "supervisor")

# ---- 编译并运行 ----
app = graph.compile()

result = app.invoke({
    "messages": [HumanMessage(content="写一篇关于 LangChain 的博客文章")],
    "topic": "LangChain 入门指南",
    "research": "",
    "draft": "",
    "final_article": "",
    "next_agent": "",
})

print("=== 最终文章 ===")
print(result["final_article"])
```

---

## 常见错误

### 1. 状态字段不一致

```python
# 错误：不同 Agent 使用不同的状态字段名
def agent_a(state):
    return {"data": "..."}  # 使用 "data"

def agent_b(state):
    return {"result": "..."}  # 使用 "result"，与 agent_a 不同

# 正确：所有 Agent 使用统一的状态字段
def agent_a(state):
    return {"shared_data": "..."}

def agent_b(state):
    return {"shared_data": "..."}
```

### 2. 忘记处理边界情况

```python
# 错误：Supervisor 可能返回无效的 Agent 名
def supervisor(state):
    response = model.invoke(...)
    return {"next_agent": response.content}  # 可能是无效值

# 正确：添加默认值和验证
def supervisor(state):
    response = model.invoke(...)
    agent = response.content.strip().lower()
    valid_agents = ["researcher", "writer", "editor"]
    return {"next_agent": agent if agent in valid_agents else "writer"}
```

### 3. 无限循环

```python
# 错误：没有退出条件
graph.add_conditional_edges(
    "reviewer",
    lambda state: "writer" if "不满意" in state["feedback"] else "end",
)

# 正确：添加最大迭代次数保护
def should_continue(state):
    if state.get("iteration", 0) >= 3:
        return "end"
    if "不满意" in state.get("feedback", ""):
        return "continue"
    return "end"
```

---

## 最佳实践

### 1. 选择合适的协作模式

```
简单任务（1-2个角色）  --> Supervisor 模式
需要频繁交互          --> Collaborative 模式
大型复杂系统          --> Hierarchical 模式
并行子任务            --> Send 动态分派
```

### 2. 状态设计要统一

```python
# 所有 Agent 共享同一个状态类型
class UnifiedState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    # 共享数据
    shared_context: str
    # 流程控制
    current_phase: str
    iteration_count: int
```

### 3. Agent 命名要清晰

```python
# 好：使用角色名称
graph.add_node("researcher", researcher_func)
graph.add_node("writer", writer_func)
graph.add_node("editor", editor_func)

# 不好：使用通用名称
graph.add_node("agent1", researcher_func)
graph.add_node("agent2", writer_func)
```

### 4. 为 Supervisor 提供清晰的指令

```python
# 好：明确列出所有可选 Agent 及其职责
system_prompt = """你是协调员，请根据任务选择合适的专家：
- researcher: 负责信息收集和调研
- writer: 负责内容创作和写作
- editor: 负责审阅和修改
只回复专家名称。"""

# 不好：指令模糊
system_prompt = "处理用户请求"
```

---

## 多 Agent 实战案例：智能软件开发团队

以下是一个完整的多 Agent 协作案例，模拟软件开发团队的工作流程：

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 定义状态
class DevTeamState(TypedDict):
    requirement: str
    prd: str
    architecture: dict
    frontend_code: str
    backend_code: str
    test_result: dict
    status: str

# 产品经理 Agent
def product_manager(state: DevTeamState):
    model = init_chat_model("groq:llama-3.3-70b-versatile")
    response = model.invoke(f"""
    你是产品经理，负责分析需求并输出PRD文档。

    需求：{state['requirement']}

    请输出：
    1. 功能需求列表
    2. 非功能需求
    3. 用户故事
    """)
    return {"prd": response.content, "status": "prd_complete"}

# 架构师 Agent
def architect(state: DevTeamState):
    model = init_chat_model("groq:llama-3.3-70b-versatile")
    response = model.invoke(f"""
    你是架构师，负责设计系统架构。

    PRD：{state['prd']}

    请输出JSON格式的架构设计：
    {{
        "frontend_spec": "前端技术方案",
        "backend_spec": "后端技术方案",
        "database": "数据库设计",
        "api": "API接口列表"
    }}
    """)
    import json
    architecture = json.loads(response.content)
    return {"architecture": architecture, "status": "architectured"}

# 开发 Agent
def developer(state: DevTeamState):
    model = init_chat_model("groq:llama-3.3-70b-versatile")
    response = model.invoke(f"""
    你是开发工程师，负责编写代码。

    前端需求：{state['architecture']['frontend_spec']}
    后端需求：{state['architecture']['backend_spec']}

    请生成核心代码。
    """)
    return {"frontend_code": "// React code", "backend_code": "// FastAPI code", "status": "developed"}

# 测试 Agent
def tester(state: DevTeamState):
    model = init_chat_model("groq:llama-3.3-70b-versatile")
    response = model.invoke(f"""
    你是测试工程师，负责代码审查和测试。

    前端代码：{state['frontend_code']}
    后端代码：{state['backend_code']}

    请审查代码并给出测试结果。
    """)
    return {"test_result": {"passed": True, "issues": []}, "status": "tested"}

# 构建工作流图
graph = StateGraph(DevTeamState)
graph.add_node("product_manager", product_manager)
graph.add_node("architect", architect)
graph.add_node("developer", developer)
graph.add_node("tester", tester)

graph.add_edge(START, "product_manager")
graph.add_edge("product_manager", "architect")
graph.add_edge("architect", "developer")
graph.add_edge("developer", "tester")
graph.add_edge("tester", END)

workflow = graph.compile()

# 执行
result = workflow.invoke({
    "requirement": "开发一个AI聊天机器人网站",
    "status": "started"
})
```

---

## 多 Agent 协作的三大挑战

### 挑战一：通信开销

多个 Agent 之间需要频繁通信，每次通信都要调用 LLM，成本和延迟都很高。

**解决方案：** 使用结构化消息，Agent 直接处理结构化数据，只在必要时调用 LLM。

```python
class Message:
    def __init__(self, sender, receiver, content, message_type):
        self.sender = sender
        self.receiver = receiver
        self.content = content  # 结构化数据，不需要LLM理解
        self.type = message_type  # "task", "result", "question"
```

### 挑战二：死锁和循环依赖

两个 Agent 互相等待对方的结果，导致死锁。

**解决方案：** 设置超时和 fallback 机制。

```python
import time

def send_and_wait(target_agent, message, timeout=30):
    start_time = time.time()
    target_agent.receive(message)

    while time.time() - start_time < timeout:
        if target_agent.has_response():
            return target_agent.get_response()
        time.sleep(0.1)

    return {"error": "Timeout", "fallback": "使用默认值"}
```

### 挑战三：结果冲突

不同 Agent 给出不同的答案，需要仲裁机制。

**解决方案：** 投票机制或专家仲裁。

```python
def resolve_conflict(opinions):
    # 方法1：加权投票
    votes = {"agree": 0, "disagree": 0}
    for opinion in opinions:
        if opinion["stance"] == "positive":
            votes["agree"] += opinion["confidence"]
        else:
            votes["disagree"] += opinion["confidence"]

    return "采纳方案" if votes["agree"] > votes["disagree"] else "否决方案"
```

---

## 多 Agent 通信模式对比

| 模式 | 特点 | 适用场景 | 实现复杂度 |
|------|------|---------|-----------|
| 层级结构 | 有明确上下级，管理者分配任务 | 层次清晰的任务 | 中等 |
| 平等协作 | Agents 地位平等，相互协商 | 需要多角度思考的复杂问题 | 高 |
| 流水线 | 固定处理顺序，每个 Agent 专注一个阶段 | 有明确步骤的任务 | 低 |

---

## 练习题

### 练习1：双 Agent 对话

构建一个两个 Agent 互相讨论的系统：
- Agent A 持支持观点
- Agent B 持反对观点
- 轮流发言 3 轮后结束

```python
# 在此编写你的代码
```

### 练习2：并行调研 + 汇总

使用 Send 实现并行调研多个主题，然后汇总结果：
1. 接收用户输入的多个主题
2. 为每个主题创建独立的调研 Agent
3. 并行执行调研
4. 汇总所有调研结果

```python
# 在此编写你的代码
```

### 练习3：三层 Supervisor

构建一个三层的 Supervisor 系统：
- 顶层 Supervisor 决定领域（技术/商务）
- 中层 Supervisor 分配具体任务
- 底层 Agent 执行具体工作

```python
# 在此编写你的代码
```

---

**相关章节**：
- [16-LangGraph基础](./16-LangGraph基础.md) - LangGraph 基础概念
- [18-条件路由](./18-条件路由.md) - 条件路由详解
