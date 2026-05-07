# Agent 基础

## 目录

- [什么是 Agent](#什么是-agent)
- [Agent vs Chain 的区别](#agent-vs-chain-的区别)
- [create_agent() API 详解](#create_agent-api-详解)
- [Agent 执行流程](#agent-执行流程)
- [检查执行详情](#检查执行详情)
- [多轮对话 Agent](#多轮对话-agent)
- [Agent 构建最佳实践](#agent-构建最佳实践)
- [常见错误](#常见错误)
- [最佳实践](#最佳实践)
- [练习题](#练习题)

---

## 什么是 Agent

### Agent 的定义

Agent（智能代理）是一种**能自主决策、使用工具的 AI 系统**。与传统的 Chain（链）不同，
Agent 不需要预定义固定的执行流程，而是根据用户的问题**动态决定**下一步做什么。

### Agent 的核心能力

```
┌─────────────────────────────────────────────┐
│              Agent 核心能力                  │
├─────────────────────────────────────────────┤
│  1. 推理（Reasoning）                        │
│     理解用户意图，分析问题                    │
│                                             │
│  2. 决策（Decision Making）                  │
│     决定是否需要工具，选择哪个工具            │
│                                             │
│  3. 工具使用（Tool Usage）                   │
│     调用外部工具获取信息或执行操作            │
│                                             │
│  4. 迭代执行（Iteration）                    │
│     根据工具结果继续推理，直到任务完成        │
│                                             │
│  5. 自我纠正（Self-Correction）              │
│     发现错误后调整策略                       │
└─────────────────────────────────────────────┘
```

### Agent 的应用场景

- **问答系统**：需要搜索外部知识来回答问题
- **数据分析**：需要调用计算工具处理数据
- **代码助手**：需要执行代码、查询文档
- **客服系统**：需要查询订单、处理退款等操作
- **研究助手**：需要搜索、整理、分析信息

---

## Agent vs Chain 的区别

### Chain（链）：固定流程

```
Chain 的执行流程（固定）：

用户输入
    │
    ▼
┌──────────┐
│ 步骤1    │  ← 固定
│ 提取关键词│
└────┬─────┘
     │
     ▼
┌──────────┐
│ 步骤2    │  ← 固定
│ 搜索知识库│
└────┬─────┘
     │
     ▼
┌──────────┐
│ 步骤3    │  ← 固定
│ 生成回答  │
└────┬─────┘
     │
     ▼
  输出回答
```

### Agent（代理）：动态决策

```
Agent 的执行流程（动态）：

用户输入
    │
    ▼
┌──────────┐
│ LLM 推理 │  ← 动态决策
└────┬─────┘
     │
     ├─── 需要搜索？ ──→ 调用搜索工具 ──→ 获取结果 ──→ 继续推理
     │
     ├─── 需要计算？ ──→ 调用计算器 ──→ 获取结果 ──→ 继续推理
     │
     ├─── 信息足够？ ──→ 生成最终回答
     │
     └─── 需要更多信息？ ──→ 继续调用工具 ──→ ...
```

### 关键区别对比

| 特性 | Chain | Agent |
|------|-------|-------|
| 执行流程 | 固定、预定义 | 动态、自主决策 |
| 工具使用 | 按固定顺序调用 | 根据需要选择调用 |
| 灵活性 | 低 | 高 |
| 可预测性 | 高 | 低 |
| 适用场景 | 流程固定的简单任务 | 需要推理的复杂任务 |
| 实现复杂度 | 低 | 中 |

### 选择指南

```
需要使用 Agent 还是 Chain？

问题：
1. 任务流程是否固定？
   - 是 → Chain
   - 否 → 继续

2. 是否需要根据中间结果决定下一步？
   - 是 → Agent
   - 否 → Chain

3. 是否需要调用多个工具？
   - 是 → Agent（动态选择）
   - 否 → Chain（固定调用）

4. 是否需要多轮推理？
   - 是 → Agent
   - 否 → Chain
```

---

## create_agent() API 详解

`create_agent()` 是 LangChain 1.0 中创建 Agent 的核心 API，替代了旧的 `create_react_agent()`。

### 基本语法

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,           # LLM 模型
    tools=[...],           # 工具列表
    system_prompt="...",   # 系统提示词
)
```

### 参数详解

#### model 参数

指定 Agent 使用的 LLM 模型。

```python
from langchain.chat_models import init_chat_model

# 方式1：传入模型 ID 字符串
agent = create_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[...],
    system_prompt="..."
)

# 方式2：传入已初始化的模型对象
model = init_chat_model("groq:llama-3.3-70b-versatile")
agent = create_agent(
    model=model,
    tools=[...],
    system_prompt="..."
)
```

#### tools 参数

传入工具列表，Agent 可以自主决定何时调用这些工具。

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """获取天气信息。"""
    return f"{city}：晴天，25°C"

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。"""
    return str(eval(expression))

# 将工具列表传给 Agent
agent = create_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[get_weather, calculator],  # 工具列表
    system_prompt="你是一个智能助手，可以查询天气和进行计算。"
)
```

#### system_prompt 参数

定义 Agent 的角色、行为规则和可用工具的使用说明。

```python
# 简单的系统提示
agent = create_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[get_weather, calculator],
    system_prompt="你是一个智能助手。"
)

# 详细的系统提示（推荐）
agent = create_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[get_weather, calculator],
    system_prompt="""你是一个专业的智能助手，具有以下能力：

1. 天气查询：可以查询国内外城市的天气信息
2. 数学计算：可以进行各种数学运算

使用规则：
- 用户问天气时，使用天气工具
- 用户需要计算时，使用计算器工具
- 回答要简洁明了，使用中文
- 如果不确定，诚实地说不知道"""
)
```

#### checkpointer 参数（可选）

用于持久化 Agent 的对话状态，支持断点续传和多轮对话。

```python
from langgraph.checkpoint.memory import MemorySaver

# 创建内存检查点
memory = MemorySaver()

agent = create_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[get_weather, calculator],
    system_prompt="你是一个智能助手。",
    checkpointer=memory  # 可选，用于持久化状态
)
```

### create_agent() 返回值

`create_agent()` 返回的是一个可调用的对象，支持 `invoke()` 和 `stream()` 方法。

```python
agent = create_agent(...)

# invoke() - 同步调用
response = agent.invoke({
    "messages": [{"role": "user", "content": "你好"}]
})

# stream() - 流式调用
for chunk in agent.stream({
    "messages": [{"role": "user", "content": "你好"}]
}):
    print(chunk)
```

---

## Agent 执行流程

### 详细执行步骤

```
用户输入："北京天气怎么样？"
    │
    ▼
步骤1：构造消息列表
    messages = [
        SystemMessage("你是一个智能助手..."),
        HumanMessage("北京天气怎么样？")
    ]
    │
    ▼
步骤2：调用 Agent
    response = agent.invoke({"messages": messages})
    │
    ▼
步骤3：LLM 推理
    LLM 分析用户意图：需要查询天气
    │
    ▼
步骤4：LLM 决定调用工具
    tool_calls = [{
        "name": "get_weather",
        "args": {"city": "北京"},
        "id": "call_abc123"
    }]
    │
    ▼
步骤5：Agent 框架自动执行工具
    result = get_weather(city="北京")
    result = "北京：晴天，25°C"
    │
    ▼
步骤6：将工具结果加入消息列表
    messages.append(ToolMessage("北京：晴天，25°C", tool_call_id="call_abc123"))
    │
    ▼
步骤7：再次调用 LLM
    LLM 基于工具结果生成最终回答
    │
    ▼
步骤8：返回最终结果
    response["messages"][-1].content = "北京今天天气晴朗，气温25°C。"
```

### Agent 执行流程图

```
┌──────────────────────────────────────────────────────────────┐
│                     Agent 执行循环                           │
│                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐ │
│  │  用户    │───→│  LLM    │───→│  工具   │───→│  结果    │ │
│  │  输入    │    │  推理   │    │  执行   │    │  处理    │ │
│  └─────────┘    └────┬────┘    └─────────┘    └────┬─────┘ │
│                      │                              │       │
│                      │    ┌─────────────────────────┘       │
│                      │    │                                 │
│                      ▼    ▼                                 │
│                 ┌──────────────┐                            │
│                 │  是否需要    │                            │
│                 │  继续？      │                            │
│                 └──────┬───────┘                            │
│                        │                                    │
│              ┌─────────┴─────────┐                          │
│              │                   │                          │
│              ▼                   ▼                          │
│         需要继续             任务完成                        │
│         (回到LLM)           (返回结果)                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 检查执行详情

### 通过 response["messages"] 查看完整执行过程

```python
"""
检查 Agent 执行详情
通过 response["messages"] 查看每一步的执行过程
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()

# 定义工具
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。

    Args:
        city: 城市名称
    """
    weather_data = {"北京": "晴天，25°C", "上海": "多云，22°C"}
    return weather_data.get(city, f"未找到{city}的天气")

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。

    Args:
        expression: 数学表达式
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算错误：{e}"


# 创建 Agent
model = init_chat_model("groq:llama-3.3-70b-versatile")
agent = create_agent(
    model=model,
    tools=[get_weather, calculator],
    system_prompt="你是一个智能助手，可以查询天气和进行计算。"
)

# 调用 Agent
response = agent.invoke({
    "messages": [{"role": "user", "content": "北京天气怎么样？顺便帮我算一下 15 * 23"}]
})

# 检查执行详情
print("=" * 60)
print("Agent 执行详情")
print("=" * 60)

for i, msg in enumerate(response["messages"]):
    print(f"\n--- 消息 {i+1} ---")
    print(f"类型: {msg.type}")

    if hasattr(msg, 'content') and msg.content:
        print(f"内容: {msg.content[:200]}")

    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        print("工具调用:")
        for tc in msg.tool_calls:
            print(f"  - {tc['name']}({tc['args']})")

    if hasattr(msg, 'tool_call_id'):
        print(f"工具调用ID: {msg.tool_call_id}")

print("\n" + "=" * 60)
print(f"最终回答: {response['messages'][-1].content}")
```

### 消息类型解读

```
response["messages"] 中的消息序列：

1. HumanMessage     ← 用户输入
   "北京天气怎么样？顺便帮我算一下 15 * 23"

2. AIMessage        ← AI 决定调用工具（包含 tool_calls）
   tool_calls: [
     {name: "get_weather", args: {city: "北京"}},
     {name: "calculator", args: {expression: "15 * 23"}}
   ]

3. ToolMessage      ← get_weather 工具的结果
   "北京：晴天，25°C"

4. ToolMessage      ← calculator 工具的结果
   "345"

5. AIMessage        ← AI 的最终回复
   "北京今天天气晴朗，气温25°C。15 × 23 = 345。"
```

---

## 多轮对话 Agent

### 使用 MemorySaver 实现多轮对话

```python
"""
多轮对话 Agent
使用 MemorySaver 保存对话状态
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

# 定义工具
@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。

    Args:
        city: 城市名称
    """
    weather_data = {"北京": "晴天，25°C", "上海": "多云，22°C"}
    return weather_data.get(city, f"未找到{city}的天气")


# 创建带记忆的 Agent
model = init_chat_model("groq:llama-3.3-70b-versatile")
memory = MemorySaver()

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一个友好的智能助手。",
    checkpointer=memory
)

# 多轮对话
thread_id = "user_123"  # 用户标识
config = {"configurable": {"thread_id": thread_id}}

# 第1轮
print("第1轮：")
response1 = agent.invoke(
    {"messages": [{"role": "user", "content": "你好，我叫小明"}]},
    config=config
)
print(f"AI: {response1['messages'][-1].content}")

# 第2轮
print("\n第2轮：")
response2 = agent.invoke(
    {"messages": [{"role": "user", "content": "你还记得我叫什么吗？"}]},
    config=config
)
print(f"AI: {response2['messages'][-1].content}")

# 第3轮
print("\n第3轮：")
response3 = agent.invoke(
    {"messages": [{"role": "user", "content": "北京天气怎么样？"}]},
    config=config
)
print(f"AI: {response3['messages'][-1].content}")
```

### MemorySaver 的作用

```
没有 MemorySaver：
  每次调用都是独立的，Agent 不记得之前的对话

  第1轮：agent.invoke("我叫小明")  → "你好小明！"
  第2轮：agent.invoke("我叫什么")  → "我不知道..."  ← 失忆

有 MemorySaver：
  MemorySaver 自动保存和恢复对话历史

  第1轮：agent.invoke("我叫小明", config)  → "你好小明！"
         MemorySaver 保存：thread_id → [HumanMessage, AIMessage]

  第2轮：agent.invoke("我叫什么", config)
         MemorySaver 恢复：thread_id → [HumanMessage, AIMessage]
         + 新消息 → "你叫小明！"  ← 记住了
```

---

## Agent 构建最佳实践

### 1. 选择合适的模型

```python
# 简单任务：使用小模型（速度快、成本低）
agent = create_agent(
    model="groq:llama3-8b-8192",
    tools=[...],
    system_prompt="..."
)

# 复杂任务：使用大模型（质量高）
agent = create_agent(
    model="groq:llama-3.3-70b-versatile",
    tools=[...],
    system_prompt="..."
)
```

### 2. 编写清晰的系统提示

```python
# ❌ 不好的系统提示
system_prompt = "你是助手"

# ✅ 好的系统提示
system_prompt = """你是一个专业的客户服务助手。

你的职责：
1. 回答客户关于产品的问题
2. 帮助客户查询订单状态
3. 处理退换货请求

使用规则：
- 使用中文回答
- 回答要专业、礼貌
- 不确定时，建议客户联系人工客服
- 涉及金额时要仔细核对"""
```

### 3. 工具设计原则

```python
# 每个工具职责单一
@tool
def query_order(order_id: str) -> str:
    """查询订单状态。"""
    ...

@tool
def cancel_order(order_id: str, reason: str) -> str:
    """取消订单。"""
    ...

# 而不是一个工具做所有事情
@tool
def manage_order(action: str, order_id: str) -> str:  # ❌ 太复杂
    ...
```

### 4. 错误处理

```python
@tool
def safe_tool(param: str) -> str:
    """一个安全的工具。"""
    try:
        # 工具逻辑
        result = do_something(param)
        return f"成功：{result}"
    except ValueError as e:
        return f"参数错误：{e}"
    except Exception as e:
        return f"执行失败：{e}"
```

---

## 常见错误

### 错误 1：忘记传 messages 参数

```python
# ❌ 错误：直接传字符串
response = agent.invoke("你好")

# ✅ 正确：传入 messages 字典
response = agent.invoke({
    "messages": [{"role": "user", "content": "你好"}]
})
```

### 错误 2：获取最终回答的方式错误

```python
response = agent.invoke({
    "messages": [{"role": "user", "content": "你好"}]
})

# ❌ 错误：直接访问 content
print(response.content)  # 错误！response 不是 AIMessage

# ✅ 正确：从 messages 中获取最后一条
print(response["messages"][-1].content)
```

### 错误 3：多轮对话时忘记传 config

```python
memory = MemorySaver()
agent = create_agent(..., checkpointer=memory)

# ❌ 错误：没有传 config
response1 = agent.invoke({"messages": [{"role": "user", "content": "我叫小明"}]})
response2 = agent.invoke({"messages": [{"role": "user", "content": "我叫什么"}]})
# response2 不记得小明，因为没有 thread_id

# ✅ 正确：传入 config
config = {"configurable": {"thread_id": "user_123"}}
response1 = agent.invoke({"messages": [...]}, config=config)
response2 = agent.invoke({"messages": [...]}, config=config)
# response2 记得小明
```

### 错误 4：工具返回非字符串

```python
# ❌ 错误
@tool
def get_count() -> int:
    """获取数量。"""
    return 42  # 返回 int

# ✅ 正确
@tool
def get_count() -> str:
    """获取数量。"""
    return "数量为 42"  # 返回 str
```

### 错误 5：系统提示中没有说明工具用途

```python
# ❌ 不好：系统提示没有提到工具
agent = create_agent(
    model=model,
    tools=[get_weather, calculator],
    system_prompt="你是一个助手。"  # 没说可以查天气和计算
)

# ✅ 好：系统提示说明可用工具
agent = create_agent(
    model=model,
    tools=[get_weather, calculator],
    system_prompt="你是一个智能助手，可以查询天气信息和进行数学计算。"
)
```

---

## 最佳实践

1. **选择合适的模型**：简单任务用小模型，复杂任务用大模型。

2. **编写详细的系统提示**：说明 Agent 的角色、能力、行为规则。

3. **工具职责单一**：每个工具只做一件事，避免过于复杂。

4. **使用 MemorySaver**：需要多轮对话时，使用 `checkpointer` 参数。

5. **检查执行详情**：通过 `response["messages"]` 查看 Agent 的完整执行过程。

6. **错误处理**：工具内部处理异常，返回友好的错误信息。

7. **使用 thread_id**：多轮对话时，为每个用户分配唯一的 `thread_id`。

---

## Agent 四层架构深度剖析

Agent 的架构可以分为四个核心层，理解这个架构有助于设计更好的 Agent 系统：

```
┌─────────────────────────────────────────────────┐
│                 Agent 四层架构                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  第一层：感知层（Perception Layer）       │    │
│  │  接收并理解用户输入                       │    │
│  │  组件：用户输入 → LLM 理解               │    │
│  │  类比：就像人的耳朵和眼睛                 │    │
│  └─────────────────────────────────────────┘    │
│                    ↓                            │
│  ┌─────────────────────────────────────────┐    │
│  │  第二层：认知层（Cognition Layer）        │    │
│  │  分析、推理、规划                         │    │
│  │  组件：LLM Brain + 规划模块 + 推理引擎   │    │
│  │  类比：就像人的大脑                       │    │
│  └─────────────────────────────────────────┘    │
│                    ↓                            │
│  ┌─────────────────────────────────────────┐    │
│  │  第三层：执行层（Execution Layer）        │    │
│  │  调用各种工具完成任务                     │    │
│  │  组件：工具集（搜索、代码、API 等）       │    │
│  │  类比：就像人的手脚                       │    │
│  └─────────────────────────────────────────┘    │
│                    ↓                            │
│  ┌─────────────────────────────────────────┐    │
│  │  第四层：记忆层（Memory Layer）           │    │
│  │  存储和检索信息                           │    │
│  │  组件：短期记忆 + 长期记忆                │    │
│  │  类比：就像人的记忆系统                   │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 数据流转示例

以任务「找出2024年诺贝尔物理学奖获得者，并总结他们的主要贡献」为例：

```
步骤1: 用户输入
  → 进入规划模块：识别需要「搜索」和「总结」两个步骤

步骤2: 规划完成
  → 进入推理引擎（ReAct框架）

步骤3: 第一轮思考-行动-观察循环
  Thought: "我需要搜索2024年诺贝尔物理学奖获得者"
  Action: 调用搜索工具 search("2024 Nobel Prize Physics")
  Observation: 获得搜索结果 → "John Hopfield 和 Geoffrey Hinton"

步骤4: 第二轮思考-行动-观察循环
  Thought: "我需要了解他们的贡献"
  Action: 调用搜索工具 search("Hopfield Hinton 神经网络贡献")
  Observation: 获得详细信息 → "人工神经网络和机器学习基础"

步骤5: 综合信息
  → LLM 整合所有观察结果
  → 生成结构化答案
  → 存入记忆模块（长期记忆）

步骤6: 输出结果
  → 返回完整答案给用户
```

Agent 不是一次性生成答案，而是通过多轮思考-行动-观察的循环，逐步接近最终答案。

---

## 理解 Agent 的三种视角

### 视角一：把 Agent 看作「员工」

```
你（老板）：「帮我准备明天的演讲PPT」

Agent（员工）：
  理解需求（演讲主题、目标听众）
  搜索资料（行业数据、案例）
  设计大纲（结构规划）
  制作PPT（使用工具）
  审核优化（自我检查）
  交付成果（PPT文件）
```

这个视角帮助你：设计 Agent 的职责范围、定义输入输出格式、考虑错误处理。

### 视角二：把 Agent 看作「循环系统」

```
输入 → [感知 → 思考 → 决策 → 行动 → 观察] → 输出
            ↑_______________________________|
                        反馈循环
```

这个视角帮助你：优化循环次数、设置终止条件、调试中间过程。

### 视角三：把 Agent 看作「大脑+工具」

```
大脑（LLM）：
  理解语言
  推理规划
  生成文本

    ↕ 通信

工具箱：
  搜索引擎
  计算器
  API 接口
  数据库
```

这个视角帮助你：扩展 Agent 能力（添加新工具）、优化工具选择（描述要精确）、提升执行效率（工具要快）。

---

## Agent 的五大核心挑战

### 挑战一：无限循环与任务卡死

Agent 可能陷入死循环，反复执行相同的搜索而无法得出结论。

**解决方案：**

```python
# 方案1：设置最大迭代次数
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="...",
    # LangGraph 中通过 recursion_limit 控制
)

# 方案2：优化提示词，明确终止条件
system_prompt = """
你必须在5步内完成任务。
如果5步内无法完成，请给出"基于现有信息的最佳答案"。
"""

# 方案3：实现智能终止判断
def should_continue(state):
    # 检查是否在重复相同的行动
    last_3_actions = state.history[-3:]
    if len(set(last_3_actions)) == 1:
        return False  # 终止
    return True
```

### 挑战二：工具选择错误

Agent 可能选择错误的工具，例如用搜索引擎查"2024年有多少天"而不是用计算器。

**解决方案：** 改进工具描述，添加使用示例，在 system_prompt 中明确工具使用规则。

### 挑战三：上下文窗口溢出

长对话或复杂任务会导致 Token 超出限制。

**解决方案：** 使用 `SummarizationMiddleware` 自动摘要、`trim_messages` 裁剪消息、分层记忆管理。

### 挑战四：错误处理与鲁棒性

工具调用失败、API 超时、返回格式错误等都可能导致 Agent 崩溃。

**解决方案：** 使用 `with_retry()` 重试、`with_fallbacks()` 降级、工具层面的 try-except 包装。

### 挑战五：成本控制

复杂任务可能消耗大量 Token，导致成本过高。

**解决方案：** 模型分级使用（简单任务用便宜模型）、缓存机制、批量处理、设置预算限制。

---

## 规划方法对比：ReAct vs Plan-and-Execute

| 特性 | ReAct（边想边做） | Plan-and-Execute（先计划后执行） |
|------|------------------|-------------------------------|
| 灵活性 | 可根据中间结果调整计划 | 计划固定，难以调整 |
| Token 消耗 | 每步都调用 LLM，消耗较大 | 只调用一次 LLM 规划，消耗较少 |
| 适用场景 | 探索性任务（不知道中间会遇到什么） | 流程明确的任务（步骤固定） |
| 并行能力 | 难以并行 | 可并行执行多个子任务 |

**选择建议：**
- 探索性任务 → 用 ReAct
- 流程明确的任务 → 用 Plan-and-Execute
- 复杂混合任务 → 两者结合

---

## 练习题

### 练习 1：基础 Agent
创建一个简单的 Agent，具备以下能力：
- 查询天气（使用模拟数据）
- 进行数学计算

测试 Agent 能否正确回答"北京天气怎么样？"和"计算 123 * 456"。

### 练习 2：检查执行详情
在练习 1 的基础上，打印 `response["messages"]` 中的所有消息：
- 每条消息的类型
- 消息内容
- 工具调用信息（如果有）

### 练习 3：多轮对话 Agent
使用 `MemorySaver` 创建一个支持多轮对话的 Agent：
- 第1轮：告诉 Agent 你的名字
- 第2轮：问 Agent 你的名字是什么
- 验证 Agent 能否记住

### 练习 4：多工具协作
创建一个包含 3 个以上工具的 Agent：
- 天气查询
- 计算器
- 翻译工具（模拟）

测试 Agent 能否在一个问题中同时使用多个工具。

### 练习 5：系统提示优化
对比以下两个系统提示的 Agent 表现：
- 简单版："你是助手"
- 详细版：包含角色、能力、规则的详细说明

分析详细系统提示如何影响 Agent 的行为。

---

> **下一步**：学习 Agent 循环与流式输出 → [06-Agent循环与流式输出.md](./06-Agent循环与流式输出.md)
