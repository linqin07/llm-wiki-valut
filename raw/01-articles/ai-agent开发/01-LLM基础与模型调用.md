# LLM 基础与模型调用

## 目录

- [LLM 基本概念](#llm-基本概念)
- [init_chat_model() 详解](#init_chat_model-详解)
- [invoke() 调用方法详解](#invoke-调用方法详解)
- [三种输入格式对比](#三种输入格式对比)
- [AIMessage 响应结构解析](#aimessage-响应结构解析)
- [模型参数详解](#模型参数详解)
- [多模型对比实验](#多模型对比实验)
- [错误处理](#错误处理)
- [常见错误](#常见错误)
- [最佳实践](#最佳实践)
- [练习题](#练习题)

---

## LLM 基本概念

### 什么是 LLM

LLM（Large Language Model，大语言模型）是一种基于深度学习的自然语言处理模型，
通过在海量文本数据上训练，能够理解和生成人类语言。

### 核心概念

#### Token（标记）

LLM 不直接处理文字，而是将文本分割成 **Token**（标记）来处理。

```
"你好世界" → ["你好", "世界"]           → 2 个 token
"Hello World" → ["Hello", " World"]    → 2 个 token
"I love programming" → ["I", " love", " programming"] → 3 个 token
```

**Token 与费用的关系**：
- 大多数 API 按 token 数量计费
- 输入 token 和输出 token 通常分开计费
- Groq 免费，但有速率限制（每分钟 token 数上限）

#### 上下文窗口（Context Window）

上下文窗口是 LLM 一次能处理的最大 token 数量。

```
┌─────────────────────────────────────────────┐
│            上下文窗口（Context Window）       │
│                                             │
│  [系统提示词] + [对话历史] + [当前输入] + [输出] │
│                                             │
│  ←────────── 总 token 数 ──────────────→    │
│           不能超过模型的上下文窗口大小         │
└─────────────────────────────────────────────┘
```

常见模型的上下文窗口大小：

| 模型 | 上下文窗口 | 说明 |
|------|-----------|------|
| llama-3.3-70b-versatile | 128K | Groq 推荐模型 |
| gpt-4o | 128K | OpenAI 旗舰模型 |
| gemini-2.0-flash | 1M | Google 大窗口模型 |
| deepseek-chat | 64K | DeepSeek 对话模型 |

---

## init_chat_model() 详解

`init_chat_model()` 是 LangChain 1.0 提供的**统一模型初始化函数**，
通过 Provider 前缀来指定不同的模型提供商。

### 基本语法

```python
from langchain.chat_models import init_chat_model

# 语法：init_chat_model("provider:model-name", **kwargs)
model = init_chat_model("groq:llama-3.3-70b-versatile")
```

### Provider 前缀格式

```
"provider:model-name"
  │        │
  │        └── 具体的模型名称
  └─────────── 提供商标识（groq, openai, anthropic, google-genai）
```

### 支持的 Provider

```python
# Groq（推荐，免费）
model = init_chat_model("groq:llama-3.3-70b-versatile")
model = init_chat_model("groq:llama3-8b-8192")
model = init_chat_model("groq:mixtral-8x7b-32768")

# OpenAI（需要付费）
model = init_chat_model("openai:gpt-4o")
model = init_chat_model("openai:gpt-4o-mini")

# Anthropic（需要付费）
model = init_chat_model("anthropic:claude-sonnet-4-20250514")

# Google Gemini（有免费额度）
model = init_chat_model("google-genai:gemini-2.0-flash")
```

### 模型参数配置

```python
model = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    temperature=0.7,      # 控制输出随机性（0-2）
    max_tokens=1024,      # 最大输出 token 数
    # 以下参数通常不需要设置
    # top_p=0.9,          # 核采样参数
    # timeout=30,         # 请求超时时间（秒）
)
```

---

## invoke() 调用方法详解

`invoke()` 是调用 LLM 的核心方法，接受消息列表作为输入，返回 AI 的回复。

### 基本调用

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("groq:llama-3.3-70b-versatile")

# 调用模型
response = model.invoke("你好")

# 获取回复内容
print(response.content)  # AI 的回复文本
```

### invoke() 的工作流程

```
用户输入 "你好"
      │
      ▼
┌─────────────────┐
│   invoke()      │
│                 │
│  1. 构造消息列表 │
│  2. 发送 API 请求│
│  3. 解析响应     │
│  4. 返回结果     │
└────────┬────────┘
         │
         ▼
   AIMessage 对象
   ├── content: "你好！有什么..."
   ├── response_metadata: {...}
   ├── id: "run-abc123"
   └── usage_metadata: {...}
```

---

## 三种输入格式对比

LangChain 支持三种消息输入格式，它们在功能上是等价的。

### 格式 1：纯字符串

```python
# 最简单的调用方式
response = model.invoke("你好")
```

**优点**：简洁，适合快速测试。
**缺点**：无法指定消息角色，不适合多轮对话。

### 格式 2：字典列表

```python
# 使用字典格式指定消息角色
response = model.invoke([
    {"role": "system", "content": "你是一个专业的翻译助手"},
    {"role": "user", "content": "请将以下句子翻译成英文：今天天气很好"}
])
```

**优点**：可以指定角色，格式直观。
**缺点**：没有类型检查，容易拼写错误。

### 格式 3：消息对象

```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 使用消息对象
response = model.invoke([
    SystemMessage(content="你是一个专业的翻译助手"),
    HumanMessage(content="请将以下句子翻译成英文：今天天气很好")
])
```

**优点**：有类型检查，IDE 自动补全，最安全。
**缺点**：代码稍长，需要额外 import。

### 三种格式对比表

| 格式 | 代码量 | 类型安全 | IDE支持 | 推荐场景 |
|------|--------|---------|---------|---------|
| 纯字符串 | 最少 | 无 | 差 | 快速测试 |
| 字典列表 | 中等 | 无 | 中 | 简单脚本 |
| 消息对象 | 较多 | 好 | 好 | **正式开发推荐** |

### 格式转换

```python
# 字典 → 消息对象
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

dict_msg = {"role": "user", "content": "你好"}

# 手动转换
if dict_msg["role"] == "user":
    obj_msg = HumanMessage(content=dict_msg["content"])
elif dict_msg["role"] == "system":
    obj_msg = SystemMessage(content=dict_msg["content"])

# 消息对象 → 字典
obj_msg = HumanMessage(content="你好")
dict_msg = {"role": "user", "content": obj_msg.content}
```

---

## AIMessage 响应结构解析

`invoke()` 返回的是一个 `AIMessage` 对象，包含丰富的元数据。

```python
response = model.invoke("你好")

# 1. content - AI 的回复文本
print(response.content)
# 输出：你好！有什么我可以帮助你的吗？

# 2. response_metadata - 响应元数据
print(response.response_metadata)
# 输出：{
#   'token_usage': {'prompt_tokens': 10, 'completion_tokens': 15, 'total_tokens': 25},
#   'model': 'llama-3.3-70b-versatile',
#   'finish_reason': 'stop'
# }

# 3. usage_metadata - token 使用统计
print(response.usage_metadata)
# 输出：{'input_tokens': 10, 'output_tokens': 15, 'total_tokens': 25}

# 4. id - 响应唯一标识
print(response.id)
# 输出：run-abc123-def456

# 5. type - 消息类型
print(response.type)
# 输出：ai
```

### AIMessage 结构图

```
AIMessage
├── content          → str    AI 回复的文本内容
├── type             → str    消息类型，固定为 "ai"
├── id               → str    响应的唯一标识符
├── response_metadata → dict   API 返回的元数据
│   ├── token_usage   → dict   token 使用量
│   ├── model         → str    使用的模型名称
│   └── finish_reason → str    结束原因（stop/length/tool_calls）
├── usage_metadata   → dict   简化的 token 使用统计
│   ├── input_tokens  → int    输入 token 数
│   ├── output_tokens → int    输出 token 数
│   └── total_tokens  → int    总 token 数
└── tool_calls       → list   工具调用列表（Agent 相关，详见 06 章节）
```

---

## 模型参数详解

### temperature（温度）

`temperature` 控制输出的随机性，是最常用的参数。

```python
# temperature = 0：输出最确定，适合代码生成、数据提取
model = init_chat_model("groq:llama-3.3-70b-versatile", temperature=0)

# temperature = 0.7：平衡随机性和一致性（默认推荐）
model = init_chat_model("groq:llama-3.3-70b-versatile", temperature=0.7)

# temperature = 1.5：输出更随机，适合创意写作
model = init_chat_model("groq:llama-3.3-70b-versatile", temperature=1.5)
```

```
temperature 值与输出关系图：

低 (0.0)                    中 (0.7)                    高 (1.5)
│                            │                            │
▼                            ▼                            ▼
"今天是晴天，               "今天天气不错，              "阳光像金色的
 温度 25°C。"                适合出门散步。"              蜂蜜洒满了街道。"

→ 确定性高，重复            → 平衡随机与一致             → 创意强，不可预测
→ 适合：代码、翻译          → 适合：大多数场景           → 适合：创意写作
```

### max_tokens（最大输出长度）

```python
# 限制输出长度
model = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    max_tokens=100  # 最多输出 100 个 token
)
```

### top_p（核采样）

```python
# 通常不需要修改，默认值 1.0 即可
model = init_chat_model(
    "groq:llama-3.3-70b-versatile",
    top_p=0.9  # 只从概率最高的 90% token 中采样
)
```

### 参数选择指南

| 场景 | temperature | max_tokens | top_p |
|------|------------|------------|-------|
| 代码生成 | 0-0.2 | 根据需要 | 1.0 |
| 数据提取 | 0 | 根据需要 | 1.0 |
| 日常对话 | 0.5-0.7 | 500-1000 | 1.0 |
| 创意写作 | 0.8-1.2 | 不限 | 1.0 |
| 头脑风暴 | 1.0-1.5 | 不限 | 0.95 |

---

## 多模型对比实验

以下代码演示如何对比不同模型的回答质量。

```python
"""
多模型对比实验
功能：同一问题，不同模型，对比输出差异
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

def compare_models(question: str):
    """对比多个模型对同一问题的回答"""

    models = {
        "Groq Llama-70B": "groq:llama-3.3-70b-versatile",
        "Groq Llama-8B": "groq:llama3-8b-8192",
    }

    print(f"问题：{question}")
    print("=" * 60)

    for name, model_id in models.items():
        try:
            model = init_chat_model(model_id)
            response = model.invoke(question)
            print(f"\n【{name}】")
            print(f"回答：{response.content[:200]}...")  # 截断显示
            print(f"Token 用量：{response.usage_metadata}")
        except Exception as e:
            print(f"\n【{name}】调用失败：{e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # 测试不同场景
    compare_models("用一句话解释什么是量子计算")
    compare_models("写一个 Python 函数，计算斐波那契数列第 n 项")
```

---

## 错误处理

### API Key 错误

```python
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

def safe_invoke(model_id: str, message: str):
    """安全调用 LLM，包含完整错误处理"""

    try:
        model = init_chat_model(model_id)
        response = model.invoke(message)
        return response.content

    except Exception as e:
        error_msg = str(e).lower()

        if "authentication" in error_msg or "api key" in error_msg:
            print("错误：API Key 无效或未配置")
            print("请检查 .env 文件中的 API Key")
            return None

        elif "rate" in error_msg or "limit" in error_msg:
            print("错误：请求频率超限")
            print("请稍后重试，或升级 API 额度")
            return None

        elif "timeout" in error_msg:
            print("错误：请求超时")
            print("请检查网络连接")
            return None

        else:
            print(f"未知错误：{e}")
            return None


# 使用示例
if __name__ == "__main__":
    result = safe_invoke("groq:llama-3.3-70b-versatile", "你好")
    if result:
        print(f"AI 回复：{result}")
```

### 网络超时处理

```python
import time
from langchain.chat_models import init_chat_model

def invoke_with_retry(model_id: str, message: str, max_retries: int = 3):
    """带重试机制的 LLM 调用"""

    model = init_chat_model(model_id)

    for attempt in range(max_retries):
        try:
            response = model.invoke(message)
            return response.content

        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避：1s, 2s, 4s
                print(f"调用失败，{wait_time}秒后重试（第{attempt + 1}次）...")
                time.sleep(wait_time)
            else:
                print(f"已重试 {max_retries} 次，仍然失败：{e}")
                raise


# 使用示例
if __name__ == "__main__":
    result = invoke_with_retry(
        "groq:llama-3.3-70b-versatile",
        "用一句话介绍 Python"
    )
    print(result)
```

---

## 常见错误

### 错误 1：忘记加载 .env

```python
# 错误：直接调用，没有加载环境变量
model = init_chat_model("groq:llama-3.3-70b-versatile")
response = model.invoke("你好")  # 可能报错 API Key 未找到

# 正确：先加载 .env
from dotenv import load_dotenv
load_dotenv()  # 必须在调用模型之前加载

model = init_chat_model("groq:llama-3.3-70b-versatile")
response = model.invoke("你好")
```

### 错误 2：Provider 前缀拼写错误

```python
# 错误：拼写错误
model = init_chat_model("grqo:llama-3.3-70b-versatile")  # grqo → groq
model = init_chat_model("groq:llama-3.3-70b")  # 模型名不完整

# 正确
model = init_chat_model("groq:llama-3.3-70b-versatile")
```

### 错误 3：混淆 invoke() 返回值

```python
response = model.invoke("你好")

# 错误：直接打印 response（会打印 AIMessage 对象，不是文本）
print(response)  # AIMessage(content='你好！...', ...)

# 正确：使用 .content 属性获取文本
print(response.content)  # 你好！有什么我可以帮助你的吗？
```

### 错误 4：未处理空回复

```python
# 某些情况下模型可能返回空内容
response = model.invoke("")

# 错误：假设 response.content 不为空
print(f"回复长度：{len(response.content)}")  # 可能为 0

# 正确：检查内容是否为空
if response.content:
    print(f"回复：{response.content}")
else:
    print("模型返回了空回复")
```

---

## 最佳实践

1. **始终使用 `.content` 获取回复文本**：`invoke()` 返回的是 `AIMessage` 对象，不是字符串。

2. **合理设置 temperature**：
   - 确定性任务（代码、翻译、数据提取）：`temperature=0`
   - 通用对话：`temperature=0.5-0.7`
   - 创意任务：`temperature=0.8-1.2`

3. **控制输出长度**：使用 `max_tokens` 防止输出过长，节省 token 消耗。

4. **添加错误处理**：生产环境中必须处理网络错误、API 限流等异常。

5. **监控 token 用量**：通过 `response.usage_metadata` 跟踪 token 消耗。

6. **选择合适的模型**：
   - 简单任务用小模型（速度快、成本低）
   - 复杂任务用大模型（质量高）

---

## 练习题

### 练习 1：基础调用
使用 `init_chat_model()` 和 `invoke()` 向 LLM 提问"什么是机器学习？"，打印回复内容。

### 练习 2：格式对比
分别使用三种输入格式（纯字符串、字典列表、消息对象）调用 LLM，确认它们的输出一致。

### 练习 3：参数实验
使用同一个问题，分别设置 `temperature=0` 和 `temperature=1.5`，对比输出的差异。
尝试多次调用，观察 `temperature=0` 的输出是否一致。

### 练习 4：元数据提取
调用 LLM 后，从 `response` 中提取以下信息并打印：
- AI 回复内容（content）
- 输入 token 数（input_tokens）
- 输出 token 数（output_tokens）
- 总 token 数（total_tokens）

### 练习 5：错误处理
编写一个 `safe_invoke()` 函数，能够处理以下错误：
- API Key 未配置
- 网络超时
- 速率限制（等待后重试）

---

> **下一步**：学习如何使用提示词模板来构建可复用的 LLM 调用 → [02-提示词模板.md](./02-提示词模板.md)
