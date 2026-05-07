# Agent 循环与流式输出

## 目录

- [ReAct 模式详解](#react-模式详解)
- [ReAct 执行周期的详细步骤图](#react-执行周期的详细步骤图)
- [流式输出（Streaming）](#流式输出streaming)
- [多步执行](#多步执行)
- [检查中间状态](#检查中间状态)
- [Agent 上下文中的消息类型](#agent-上下文中的消息类型)
- [最终答案位置](#最终答案位置)
- [流式输出 vs 普通调用](#流式输出-vs-普通调用)
- [常见错误](#常见错误)
- [最佳实践](#最佳实践)
- [练习题](#练习题)

---

## ReAct 模式详解

### 什么是 ReAct

ReAct（Reasoning + Acting）是一种让 LLM 结合**推理**和**行动**的框架。
它是现代 Agent 的核心执行模式。

### ReAct 的三个阶段

```
┌─────────────────────────────────────────────────┐
│                ReAct 模式                        │
│                                                  │
│   Reason（推理）                                 │
│   ├── 分析用户意图                               │
│   ├── 思考需要什么信息                           │
│   └── 决定下一步行动                             │
│                                                  │
│   Act（行动）                                    │
│   ├── 选择合适的工具                             │
│   ├── 确定工具参数                               │
│   └── 执行工具调用                               │
│                                                  │
│   Observe（观察）                                │
│   ├── 获取工具执行结果                           │
│   ├── 分析结果是否满足需求                       │
│   └── 决定是否需要继续循环                       │
│                                                  │
└─────────────────────────────────────────────────┘
```

### ReAct 与传统方法的区别

```
传统方法（只推理）：
  问：北京天气怎么样？
  答：我无法获取实时天气信息...（LLM 没有实时数据）

传统方法（只行动）：
  问：北京天气怎么样？
  答：北京：晴天，25°C。（直接返回原始数据，没有自然语言处理）

ReAct 方法（推理 + 行动）：
  问：北京天气怎么样？
  推理：用户想知道北京的天气，我需要调用天气工具
  行动：调用 get_weather("北京")
  观察：返回 "晴天，25°C"
  推理：获取到了天气信息，现在可以回答用户了
  答：北京今天天气晴朗，气温25°C，非常适合出行。
```

---

## ReAct 执行周期的详细步骤图

### 单工具调用流程

```
用户："北京天气怎么样？"
    │
    ▼
┌──────────────────────────────────────────────────────┐
│ 第1步：Reason（推理）                                 │
│                                                      │
│ LLM 内部思考：                                        │
│ "用户想知道北京的天气。我有一个 get_weather 工具，    │
│  可以用它来查询。参数应该是 city='北京'。"            │
│                                                      │
│ 输出：AIMessage with tool_calls                       │
│   tool_calls: [{name: "get_weather", args: {city: "北京"}}] │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│ 第2步：Act（行动）                                    │
│                                                      │
│ Agent 框架自动执行工具：                               │
│   result = get_weather(city="北京")                   │
│   result = "北京：晴天，25°C，湿度 40%"               │
│                                                      │
│ 生成 ToolMessage：                                    │
│   content = "北京：晴天，25°C，湿度 40%"              │
│   tool_call_id = "call_abc123"                        │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│ 第3步：Observe（观察）                                │
│                                                      │
│ LLM 收到工具结果，分析：                              │
│ "我已经获取到了北京的天气信息：晴天，25°C。           │
│  这个信息足够回答用户的问题了。"                      │
│                                                      │
│ 判断：任务完成，不需要继续循环                        │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│ 第4步：生成最终回答                                   │
│                                                      │
│ AIMessage：                                           │
│   content = "北京今天天气晴朗，气温25°C，              │
│              湿度40%，非常适合出行。"                  │
│   tool_calls = []  （没有工具调用，表示任务完成）       │
└──────────────────────────────────────────────────────┘
```

### 多工具调用流程

```
用户："北京天气怎么样？另外帮我算一下 15 * 23"
    │
    ▼
┌──────────────────────────────────────────────────────┐
│ 第1轮 Reason → Act → Observe                         │
│                                                      │
│ Reason: 需要查天气和做计算，两个任务互不影响，         │
│        可以同时调用两个工具。                          │
│                                                      │
│ Act: 同时调用两个工具                                 │
│   tool_calls: [                                      │
│     {name: "get_weather", args: {city: "北京"}},     │
│     {name: "calculator", args: {expr: "15 * 23"}}   │
│   ]                                                  │
│                                                      │
│ Observe:                                              │
│   get_weather → "北京：晴天，25°C"                    │
│   calculator → "345"                                 │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────┐
│ 最终回答                                              │
│                                                      │
│ "北京今天天气晴朗，气温25°C。                          │
│  15 × 23 = 345。"                                    │
└──────────────────────────────────────────────────────┘
```

### 需要多轮推理的复杂场景

```
用户："北京和上海哪个城市更热？差几度？"
    │
    ▼
┌─ 第1轮 ──────────────────────────────────────────────┐
│ Reason: 需要查两个城市的天气才能比较                   │
│ Act: get_weather("北京") → "晴天，25°C"               │
│      get_weather("上海") → "多云，22°C"               │
│ Observe: 北京25°C，上海22°C                          │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌─ 第2轮 ──────────────────────────────────────────────┐
│ Reason: 北京25°C > 上海22°C，差3度。                  │
│         不需要再调用工具了。                           │
│ Act: 无（不需要工具）                                 │
│ Observe: 任务完成                                     │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌─ 最终回答 ───────────────────────────────────────────┐
│ "北京更热，气温25°C；上海22°C，相差3度。"              │
└──────────────────────────────────────────────────────┘
```

---

## 流式输出（Streaming）

### 什么是流式输出

流式输出允许你**实时查看 Agent 的执行过程**，而不是等待全部完成后再返回。

```
普通调用（invoke）：
  用户发送请求 → 等待... → 一次性返回完整结果

流式调用（stream）：
  用户发送请求 → 逐步返回每个步骤的中间结果
                 ├── 步骤1: AI 开始思考...
                 ├── 步骤2: 调用天气工具...
                 ├── 步骤3: 获取结果...
                 ├── 步骤4: 生成回答...
                 └── 步骤5: "北京天气晴朗..."
```

### .stream() 方法

```python
"""
流式输出示例
使用 .stream() 方法实时查看 Agent 执行过程
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。

    Args:
        city: 城市名称
    """
    weather_data = {"北京": "晴天，25°C", "上海": "多云，22°C"}
    return weather_data.get(city, f"未找到{city}的天气")


# 创建 Agent
model = init_chat_model("groq:llama-3.3-70b-versatile")
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一个智能助手。"
)

# 流式调用
print("Agent 开始执行...")
print("=" * 50)

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "北京天气怎么样？"}]
}):
    # chunk 是一个字典，包含当前步骤的信息
    print(f"\n--- 新的 chunk ---")
    print(f"Keys: {list(chunk.keys())}")

    # 遍历 chunk 中的消息
    for key, value in chunk.items():
        if isinstance(value, list):
            for msg in value:
                if hasattr(msg, 'content') and msg.content:
                    print(f"  [{msg.type}] {msg.content[:100]}")
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tc in msg.tool_calls:
                        print(f"  [工具调用] {tc['name']}({tc['args']})")
        elif isinstance(value, dict):
            print(f"  {key}: {value}")

print("\n" + "=" * 50)
print("Agent 执行完成")
```

### Stream Chunk 的结构解析

```python
# 每个 chunk 是一个字典
# 键是节点名，值是该节点的输出

# 示例 chunk 结构：
{
    "agent": {  # Agent 节点
        "messages": [
            AIMessage(
                content="",  # 可能为空（工具调用时）
                tool_calls=[{
                    "name": "get_weather",
                    "args": {"city": "北京"},
                    "id": "call_abc123"
                }]
            )
        ]
    }
}

# 工具执行后的 chunk：
{
    "tools": {  # 工具节点
        "messages": [
            ToolMessage(
                content="北京：晴天，25°C",
                tool_call_id="call_abc123"
            )
        ]
    }
}

# 最终回答的 chunk：
{
    "agent": {
        "messages": [
            AIMessage(
                content="北京今天天气晴朗，气温25°C。",
                tool_calls=[]  # 空，表示任务完成
            )
        ]
    }
}
```

### 流式输出的 chunk 序列

```
stream() 返回的 chunk 序列：

chunk 1: {"agent": {"messages": [AIMessage(tool_calls=[...])]}}
         → AI 决定调用工具

chunk 2: {"tools": {"messages": [ToolMessage("北京：晴天，25°C")]}}
         → 工具执行结果

chunk 3: {"agent": {"messages": [AIMessage(content="北京今天天气...")]}}
         → AI 的最终回复
```

---

## 多步执行

### Agent 连续调用多个工具的场景

```python
"""
多步执行示例
Agent 在一次请求中连续调用多个工具
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。

    Args:
        city: 城市名称
    """
    weather_data = {"北京": "晴天，25°C", "上海": "多云，22°C", "广州": "阵雨，28°C"}
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

# 测试多步执行
response = agent.invoke({
    "messages": [{"role": "user", "content": "北京和上海哪个更热？差几度？"}]
})

# 分析执行过程
print("=" * 60)
print("多步执行分析")
print("=" * 60)

for i, msg in enumerate(response["messages"]):
    print(f"\n消息 {i+1} [{msg.type}]:")
    if msg.content:
        print(f"  内容: {msg.content[:150]}")
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"  工具调用: {tc['name']}({tc['args']})")

print(f"\n最终回答: {response['messages'][-1].content}")
```

### 多步执行流程图

```
用户："北京和上海哪个更热？差几度？"
    │
    ▼
┌─ 步骤1：Agent 推理 ──────────────────────────────────┐
│ 需要查两个城市的天气                                   │
│                                                      │
│ tool_calls: [                                        │
│   {name: "get_weather", args: {city: "北京"}},       │
│   {name: "get_weather", args: {city: "上海"}}        │
│ ]                                                    │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌─ 步骤2：工具执行 ────────────────────────────────────┐
│ get_weather("北京") → "晴天，25°C"                    │
│ get_weather("上海") → "多云，22°C"                    │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌─ 步骤3：Agent 再次推理 ──────────────────────────────┐
│ 北京25°C，上海22°C                                    │
│ 北京更热，差3度                                        │
│ 信息足够，生成最终回答                                 │
└──────────────────────────┬───────────────────────────┘
                           │
                           ▼
┌─ 步骤4：最终回答 ────────────────────────────────────┐
│ "北京更热，气温25°C；上海22°C，相差3度。"              │
└──────────────────────────────────────────────────────┘
```

---

## 检查中间状态

### 通过 stream chunks 查看每一步

```python
"""
检查中间状态示例
通过 stream 实时查看 Agent 的每一步执行
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。"""
    weather_data = {"北京": "晴天，25°C", "上海": "多云，22°C"}
    return weather_data.get(city, f"未找到{city}的天气")

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。"""
    return str(eval(expression))


model = init_chat_model("groq:llama-3.3-70b-versatile")
agent = create_agent(
    model=model,
    tools=[get_weather, calculator],
    system_prompt="你是一个智能助手。"
)

# 流式执行并检查中间状态
print("开始执行...")
step = 0

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "北京天气怎么样？15+23等于多少？"}]
}):
    step += 1
    print(f"\n{'='*40}")
    print(f"步骤 {step}")
    print(f"{'='*40}")

    for node_name, node_data in chunk.items():
        print(f"节点: {node_name}")

        if "messages" in node_data:
            for msg in node_data["messages"]:
                if msg.type == "ai":
                    if msg.tool_calls:
                        print("  AI 决定调用工具:")
                        for tc in msg.tool_calls:
                            print(f"    - {tc['name']}({tc['args']})")
                    else:
                        print(f"  AI 回复: {msg.content[:100]}")

                elif msg.type == "tool":
                    print(f"  工具结果: {msg.content[:100]}")

print(f"\n{'='*40}")
print("执行完成")
```

---

## Agent 上下文中的消息类型

### 消息类型详解

```python
"""
Agent 执行过程中出现的消息类型
"""

# 1. HumanMessage - 用户输入
#    出现在：对话开始
#    type: "human"
#    content: 用户的问题

# 2. AIMessage（带 tool_calls）- AI 决定调用工具
#    出现在：AI 需要使用工具时
#    type: "ai"
#    content: 可能为空或思考过程
#    tool_calls: [{name, args, id}, ...]

# 3. ToolMessage - 工具返回结果
#    出现在：工具执行完成后
#    type: "tool"
#    content: 工具的执行结果
#    tool_call_id: 关联到哪个工具调用

# 4. AIMessage（不带 tool_calls）- AI 的最终回复
#    出现在：任务完成时
#    type: "ai"
#    content: 最终回答
#    tool_calls: []  （空列表表示不需要工具）
```

### 消息序列示例

```python
# 完整的消息序列示例

messages = [
    # 1. 用户输入
    HumanMessage(content="北京天气怎么样？"),

    # 2. AI 决定调用工具
    AIMessage(
        content="",  # 或思考过程
        tool_calls=[{
            "name": "get_weather",
            "args": {"city": "北京"},
            "id": "call_abc123"
        }]
    ),

    # 3. 工具执行结果
    ToolMessage(
        content="北京：晴天，25°C",
        tool_call_id="call_abc123"
    ),

    # 4. AI 的最终回复
    AIMessage(
        content="北京今天天气晴朗，气温25°C。",
        tool_calls=[]  # 空列表，任务完成
    )
]
```

### 消息类型关系图

```
HumanMessage (用户输入)
    │
    ▼
AIMessage (带 tool_calls)  ←── AI 决定调用工具
    │
    ▼
ToolMessage (工具结果)     ←── 工具执行完成
    │
    ├──→ AIMessage (带 tool_calls)  ←── 需要继续调用工具（循环）
    │         │
    │         ▼
    │    ToolMessage ...
    │
    └──→ AIMessage (不带 tool_calls) ←── 任务完成，生成最终回复
```

---

## 最终答案位置

### 如何获取最终回答

```python
"""
获取 Agent 最终回答的正确方式
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool

load_dotenv()

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息。"""
    return f"{city}：晴天，25°C"


model = init_chat_model("groq:llama-3.3-70b-versatile")
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是一个智能助手。"
)

# 调用 Agent
response = agent.invoke({
    "messages": [{"role": "user", "content": "北京天气怎么样？"}]
})

# 获取最终回答（推荐方式）
final_answer = response["messages"][-1].content
print(f"最终回答: {final_answer}")

# 也可以遍历所有消息找到最后一个 AIMessage
for msg in reversed(response["messages"]):
    if msg.type == "ai" and msg.content:
        print(f"AI 回复: {msg.content}")
        break
```

### 最终回答位置图

```
response["messages"] 的结构：

[0] HumanMessage     "北京天气怎么样？"
[1] AIMessage        tool_calls: [{name: "get_weather", ...}]
[2] ToolMessage      "北京：晴天，25°C"
[3] AIMessage        "北京今天天气晴朗，气温25°C。"  ← 这是最终回答

获取方式：response["messages"][-1].content
```

---

## 流式输出 vs 普通调用

### 对比表

| 特性 | invoke() | stream() |
|------|----------|----------|
| 返回方式 | 一次性返回完整结果 | 逐步返回中间结果 |
| 用户体验 | 需要等待 | 实时反馈 |
| 适用场景 | 后台处理、批量任务 | 交互式应用、聊天界面 |
| 实现复杂度 | 简单 | 中等 |
| 错误处理 | 简单 | 需要处理中断 |

### invoke() 示例

```python
# 普通调用：等待完成后一次性返回
response = agent.invoke({
    "messages": [{"role": "user", "content": "北京天气怎么样？"}]
})

# 直接获取最终结果
print(response["messages"][-1].content)
```

### stream() 示例

```python
# 流式调用：实时查看执行过程
final_content = ""

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "北京天气怎么样？"}]
}):
    for node_name, node_data in chunk.items():
        if "messages" in node_data:
            for msg in node_data["messages"]:
                if msg.type == "ai" and msg.content:
                    # 实时打印 AI 的回复
                    print(msg.content, end="", flush=True)
                    final_content = msg.content

print()  # 换行
```

### 选择指南

```
应该使用 invoke() 还是 stream()？

场景分析：
1. 是否需要实时显示执行过程？
   - 是 → stream()
   - 否 → invoke()

2. 是否在交互式界面中使用？
   - 是 → stream()（提供更好的用户体验）
   - 否 → invoke()

3. 是否需要处理长时间运行的任务？
   - 是 → stream()（可以显示进度）
   - 否 → invoke()

4. 是否在后台批量处理？
   - 是 → invoke()（更简单）
   - 否 → 根据其他条件选择
```

---

## 常见错误

### 错误 1：混淆 invoke() 和 stream() 的返回格式

```python
# ❌ 错误：把 stream() 的返回当作完整结果
response = agent.stream({...})
print(response["messages"][-1].content)  # 错误！stream 返回的是生成器

# ✅ 正确：遍历 stream() 的返回
for chunk in agent.stream({...}):
    # 处理每个 chunk
    pass
```

### 错误 2：stream() 中不处理所有 chunk 类型

```python
# ❌ 错误：只处理 Agent 节点的 chunk
for chunk in agent.stream({...}):
    if "agent" in chunk:  # 忽略了 "tools" 节点
        print(chunk["agent"])

# ✅ 正确：处理所有节点类型
for chunk in agent.stream({...}):
    for node_name, node_data in chunk.items():
        print(f"节点: {node_name}")
        # 处理 node_data
```

### 错误 3：获取最终回答时索引错误

```python
response = agent.invoke({...})

# ❌ 错误：假设最后一条消息一定是 AI 回复
answer = response["messages"][-1].content  # 可能是 ToolMessage！

# ✅ 正确：检查消息类型
last_msg = response["messages"][-1]
if last_msg.type == "ai":
    answer = last_msg.content
else:
    # 遍历找到最后一个 AI 消息
    for msg in reversed(response["messages"]):
        if msg.type == "ai" and msg.content:
            answer = msg.content
            break
```

### 错误 4：在流式输出中累加工具调用结果

```python
# ❌ 错误：尝试在 stream 中手动执行工具
for chunk in agent.stream({...}):
    for node_name, node_data in chunk.items():
        if "messages" in node_data:
            for msg in node_data["messages"]:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    # 不需要手动执行！Agent 框架会自动执行
                    for tc in msg.tool_calls:
                        result = get_weather(tc["args"])  # 多余！
```

### 错误 5：忽略 stream chunk 中的空消息

```python
# ❌ 错误：不检查 content 是否为空
for chunk in agent.stream({...}):
    for node_name, node_data in chunk.items():
        for msg in node_data["messages"]:
            print(msg.content)  # 可能为空字符串！

# ✅ 正确：检查 content 是否为空
for chunk in agent.stream({...}):
    for node_name, node_data in chunk.items():
        if "messages" in node_data:
            for msg in node_data["messages"]:
                if msg.content:  # 检查是否为空
                    print(msg.content)
```

---

## 最佳实践

1. **选择合适的调用方式**：
   - 交互式应用使用 `stream()`
   - 后台处理使用 `invoke()`

2. **正确获取最终回答**：使用 `response["messages"][-1].content`

3. **处理所有消息类型**：不要假设消息类型，始终检查 `msg.type`

4. **流式输出中检查空值**：`msg.content` 可能为空字符串

5. **不要手动执行工具**：Agent 框架会自动执行工具调用

6. **监控执行过程**：通过 `response["messages"]` 或 stream chunks 查看 Agent 的推理过程

7. **错误处理**：捕获并处理工具执行中的异常

---

## 练习题

### 练习 1：基础 ReAct
创建一个 Agent，测试以下场景：
- 单工具调用："北京天气怎么样？"
- 多工具调用："北京天气和 15+23 的结果"
- 无工具调用："你好"

分析每个场景中 `response["messages"]` 的消息序列。

### 练习 2：流式输出
使用 `.stream()` 方法调用 Agent，实时打印执行过程：
- 打印每个 chunk 的节点名称
- 打印 AI 的工具调用决策
- 打印工具执行结果
- 打印最终回答

### 练习 3：多步推理
创建一个需要多步推理的场景：
- "北京和上海哪个更热？差几度？"
- 分析 Agent 是否正确地调用了两次天气工具
- 验证最终回答是否正确计算了温差

### 练习 4：消息类型分析
编写一个函数，接收 `response["messages"]`，打印：
- 每条消息的类型（human/ai/tool）
- 消息内容
- 工具调用信息（如果有）
- 工具调用 ID（如果有）

### 练习 5：流式 vs 普通对比
对同一个问题，分别使用 `invoke()` 和 `stream()` 调用 Agent：
- 对比返回结果是否一致
- 对比执行时间
- 分析两种方式的适用场景

---

> **恭喜！** 你已经完成了 LangChain & LangGraph 基础知识的学习。接下来可以进入第二阶段的实践应用模块。
