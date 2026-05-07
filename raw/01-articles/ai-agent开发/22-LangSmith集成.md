# 22 - LangSmith 集成

## 目录

- [LangSmith 是什么](#langsmith-是什么)
- [为什么需要 LangSmith](#为什么需要-langsmith)
- [环境变量配置](#环境变量配置)
- [@traceable 装饰器](#traceable-装饰器)
- [RunnableConfig](#runnableconfig)
- [Agent 执行的 Trace 可视化](#agent-执行的-trace-可视化)
- [调试技巧](#调试技巧)
- [完整代码示例](#完整代码示例)
- [常见错误](#常见错误)
- [最佳实践](#最佳实践)
- [练习题](#练习题)

---

## LangSmith 是什么

### 概念介绍

LangSmith 是 LangChain 官方提供的**可观测性平台**，用于调试、监控、评估和追踪 LLM 应用的执行过程。

```
LLM 应用
    |
    | 执行时自动上报
    v
+---+---+
|LangSmith|
|  平台   |
+---+---+
    |
    +---> Trace 追踪（查看完整执行链）
    +---> 性能监控（延迟、token 消耗）
    +---> 评估工具（质量检测）
    +--=== 数据集管理（测试用例）
```

### 核心功能

| 功能 | 说明 |
|------|------|
| Trace 追踪 | 查看完整的执行链路，包括每个步骤的输入/输出 |
| 性能监控 | 监控延迟、token 使用量、成本 |
| 评估 | 自动评估 LLM 输出质量 |
| 数据集 | 管理测试数据集 |
| Prompt 管理 | 版本管理 Prompt |
| 告警 | 异常情况自动通知 |

---

## 为什么需要 LangSmith

### LLM 应用的调试难题

```
传统软件调试：
  代码 --> 确定性输出
  断点调试、日志查看

LLM 应用调试：
  Prompt --> LLM --> 不确定性输出
  问题：
  1. 同样的输入可能得到不同输出
  2. Agent 的决策路径复杂
  3. 工具调用链路长
  4. 难以定位问题在哪一步
```

### LangSmith 解决的问题

```
没有 LangSmith:
  用户提问 --> [???] --> 错误回答
  "为什么回答错了？"  -- 无法知道

有 LangSmith:
  用户提问
      |
      v
  +---+---+
  | Step1 | LLM 思考 -> "需要搜索工具"
  +---+---+
      |
      v
  +---+---+
  | Step2 | 调用搜索工具 -> 返回结果
  +---+---+
      |
      v
  +---+---+
  | Step3 | LLM 基于结果生成回答 -> "错误答案"
  +---+---+

  问题定位：Step3 的 Prompt 不够清晰，导致 LLM 误解了搜索结果
```

---

## 环境变量配置

### 基本配置

```bash
# .env 文件
LANGSMITH_TRACING=true                # 启用追踪
LANGSMITH_API_KEY=lsv2_pt_xxxx        # API Key
LANGSMITH_PROJECT=MyLangChainProject  # 项目名称
```

### 获取 API Key

```
1. 访问 https://smith.langchain.com/
2. 注册/登录账号
3. 进入 Settings -> API Keys
4. 创建新的 API Key
5. 复制到 .env 文件
```

### Python 代码中配置

```python
import os
from dotenv import load_dotenv

load_dotenv()

# 验证配置
print(f"Tracing: {os.getenv('LANGSMITH_TRACING')}")
print(f"Project: {os.getenv('LANGSMITH_PROJECT')}")
```

### 可选配置

```bash
# 详细追踪（包含 LLM 的原始请求和响应）
LANGSMITH_TRACING_V2=true

# 自定义端点（企业私有部署）
LANGSMITH_ENDPOINT=https://api.smith.langchain.com

# 记录所有模型调用（包括嵌套的）
LANGSMITH_RECORD_ALL=true
```

---

## @traceable 装饰器

### 基本用法

`@traceable` 装饰器可以追踪任何 Python 函数的执行：

```python
from langsmith import traceable

@traceable
def my_function(input_text: str) -> str:
    """被追踪的函数"""
    result = process(input_text)
    return result

# 调用时自动上报到 LangSmith
my_function("测试输入")
```

### 自定义追踪名称

```python
@traceable(name="数据处理函数")
def process_data(data: dict) -> dict:
    # 处理逻辑
    return result

@traceable(name="LLM 调用")
def call_llm(prompt: str) -> str:
    response = model.invoke(prompt)
    return response.content
```

### 追踪嵌套函数

```python
@traceable(name="主流程")
def main_workflow(input_text: str) -> str:
    # 步骤1
    step1_result = step1(input_text)

    # 步骤2
    step2_result = step2(step1_result)

    # 步骤3
    return step3(step2_result)

@traceable(name="步骤1-预处理")
def step1(text: str) -> str:
    return text.lower()

@traceable(name="步骤2-分析")
def step2(text: str) -> str:
    return model.invoke(text).content

@traceable(name="步骤3-格式化")
def step3(text: str) -> str:
    return f"结果: {text}"

# 调用主流程，所有嵌套函数都会被追踪
main_workflow("Hello World")
```

**追踪结果在 LangSmith 中的展示：**

```
main_workflow ("Hello World")
  |
  +-- step1 ("Hello World")
  |     返回: "hello world"
  |
  +-- step2 ("hello world")
  |     |
  |     +-- LLM Call
  |     |   输入: "hello world"
  |     |   输出: "分析结果..."
  |     |
  |     返回: "分析结果..."
  |
  +-- step3 ("分析结果...")
        返回: "结果: 分析结果..."
```

### 添加元数据

```python
@traceable(
    name="文档处理",
    metadata={"version": "1.0", "env": "production"},
    tags=["document", "processing"],
)
def process_document(doc_path: str) -> str:
    # 处理文档
    return result
```

---

## RunnableConfig

### 什么是 RunnableConfig

`RunnableConfig` 是 LangChain 中用于传递运行时配置的对象，可以包含元数据、标签、回调等。

```python
from langchain_core.runnables import RunnableConfig

config = RunnableConfig(
    run_name="my_run",           # 运行名称
    tags=["tag1", "tag2"],       # 标签
    metadata={"key": "value"},   # 元数据
)
```

### 在 LLM 调用中使用

```python
from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig

model = init_chat_model("groq:llama-3.3-70b-versatile")

# 带配置的调用
config = RunnableConfig(
    run_name="用户问题回答",
    tags=["qa", "production"],
    metadata={
        "user_id": "user_123",
        "session_id": "session_456",
        "source": "web",
    }
)

response = model.invoke("什么是 LangChain?", config=config)
```

### 在 Agent 调用中使用

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[...],
    system_prompt="你是一个助手"
)

# 带配置的 Agent 调用
config = {
    "run_name": "Agent 会话",
    "tags": ["agent", "v2"],
    "metadata": {
        "user_id": "user_123",
        "feature": "chat",
    }
}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "你好"}]},
    config=config
)
```

### metadata 的最佳实践

```python
config = RunnableConfig(
    metadata={
        # 追踪信息
        "user_id": "user_123",
        "session_id": "session_abc",
        "request_id": "req_xyz",

        # 版本信息
        "app_version": "1.0.0",
        "model_version": "gpt-4o",

        # 业务信息
        "feature": "chat",
        "environment": "production",

        # A/B 测试
        "experiment": "prompt_v2",
    }
)
```

---

## Agent 执行的 Trace 可视化

### Trace 结构

在 LangSmith 中，一个完整的 Agent 执行 Trace 如下：

```
Trace: Agent 执行
├── LLM Call (思考)
│   ├── Input: [SystemMessage, HumanMessage]
│   ├── Output: AIMessage (tool_call)
│   ├── Tokens: 150
│   └── Latency: 1.2s
│
├── Tool Call (搜索)
│   ├── Input: {"query": "Python 3.12 新特性"}
│   ├── Output: "Python 3.12 引入了..."
│   └── Latency: 0.5s
│
├── LLM Call (生成回答)
│   ├── Input: [SystemMessage, HumanMessage, ToolMessage]
│   ├── Output: AIMessage
│   ├── Tokens: 300
│   └── Latency: 2.1s
│
└── Total
    ├── Total Tokens: 450
    ├── Total Latency: 3.8s
    └── Status: Success
```

### 查看 Trace

```
1. 访问 https://smith.langchain.com/
2. 选择你的项目
3. 在 "Traces" 标签页查看
4. 点击任意 Trace 查看详情
5. 展开每个步骤查看输入/输出
```

---

## 调试技巧

### 技巧1：查看完整执行链

```python
# 确保启用追踪
os.environ["LANGSMITH_TRACING"] = "true"

# 执行你的应用
result = app.invoke(input_data)

# 在 LangSmith UI 中查看完整的执行链
# 可以看到每一步的输入、输出、耗时
```

### 技巧2：定位性能瓶颈

```python
# 使用 metadata 标记关键步骤
@traceable(name="数据预处理")
def preprocess(data):
    # 可能很慢的步骤
    return processed_data

@traceable(name="LLM 调用")
def llm_call(prompt):
    # LLM 调用通常是最慢的
    return model.invoke(prompt)

# 在 LangSmith 中查看每步耗时
# 找到最慢的步骤进行优化
```

### 技巧3：分析 token 消耗

```python
# 在 LangSmith 中可以看到：
# - 每次 LLM 调用的 input/output tokens
# - 总的 token 消耗
# - 不同模型的 token 使用对比

# 优化建议：
# 1. 减少 system prompt 的长度
# 2. 限制 message history 的长度
# 3. 使用更小的模型处理简单任务
```

### 技巧4：使用 tags 过滤

```python
# 为不同类型的调用添加标签
config_tags = {
    "chat": ["chat", "user-facing"],
    "tool": ["tool", "internal"],
    "summarize": ["summarize", "batch"],
}

# 在 LangSmith UI 中按标签过滤
# 快速找到特定类型的调用
```

### 技巧5：错误追踪

```python
@traceable(name="可能失败的操作")
def risky_operation(input_data):
    try:
        result = process(input_data)
        return {"status": "success", "result": result}
    except Exception as e:
        # 错误也会被记录到 LangSmith
        return {"status": "error", "error": str(e)}

# 在 LangSmith 中可以过滤查看所有失败的调用
```

---

## 完整代码示例

### 示例1：基础追踪

```python
"""
LangSmith 基础追踪示例
"""
import os
from dotenv import load_dotenv
from langsmith import traceable
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

load_dotenv()

# 验证配置
assert os.getenv("LANGSMITH_TRACING") == "true", "请设置 LANGSMITH_TRACING=true"
assert os.getenv("LANGSMITH_API_KEY"), "请设置 LANGSMITH_API_KEY"

model = init_chat_model("groq:llama-3.3-70b-versatile")

@traceable(name="问答函数")
def answer_question(question: str) -> str:
    """被追踪的问答函数"""
    response = model.invoke([HumanMessage(content=question)])
    return response.content

@traceable(name="带预处理的问答")
def preprocess_and_answer(question: str) -> str:
    """带预处理的问答"""
    # 预处理
    cleaned = question.strip()

    # 回答
    answer = answer_question(cleaned)

    # 后处理
    return f"回答: {answer}"

# 执行
result = preprocess_and_answer("  什么是 LangChain?  ")
print(result)

# 在 LangSmith 中可以看到：
# - preprocess_and_answer 的完整调用
#   - answer_question 的子调用
#   - LLM 的具体调用详情
```

### 示例2：Agent 追踪

```python
"""
带 LangSmith 追踪的 Agent
"""
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

load_dotenv()

model = init_chat_model("groq:llama-3.3-70b-versatile")

@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"搜索结果: 关于 '{query}' 的最新信息..."

@tool
def calculate(expression: str) -> str:
    """计算数学表达式"""
    try:
        return str(eval(expression))
    except:
        return "计算错误"

# 创建 Agent
agent = create_agent(
    model=model,
    tools=[search, calculate],
    system_prompt="你是一个智能助手，可以搜索信息和进行计算。"
)

# 带追踪的调用
config = RunnableConfig(
    run_name="用户问答",
    tags=["chat", "production"],
    metadata={
        "user_id": "user_123",
        "feature": "qa",
    }
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "搜索一下 Python 3.12 的新特性"}]},
    config=config
)

print(response["messages"][-1].content)
```

### 示例3：性能监控

```python
"""
性能监控示例
追踪每个步骤的耗时和 token 消耗
"""
import os
import time
from dotenv import load_dotenv
from langsmith import traceable
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

load_dotenv()

model = init_chat_model("groq:llama-3.3-70b-versatile")

@traceable(name="LLM 调用", tags=["llm"])
def call_llm(prompt: str, model_name: str = "default") -> dict:
    """带性能监控的 LLM 调用"""
    start_time = time.time()

    response = model.invoke([HumanMessage(content=prompt)])

    elapsed = time.time() - start_time

    return {
        "response": response.content,
        "elapsed_seconds": round(elapsed, 2),
        "model": model_name,
    }

@traceable(name="批处理", tags=["batch"])
def batch_process(questions: list[str]) -> list[dict]:
    """批量处理问题"""
    results = []
    for q in questions:
        result = call_llm(q, model_name="groq:llama-3.3-70b")
        results.append(result)
    return results

# 执行批量处理
questions = [
    "什么是机器学习？",
    "什么是深度学习？",
    "什么是自然语言处理？",
]

results = batch_process(questions)
for r in results:
    print(f"耗时: {r['elapsed_seconds']}s")
```

### 示例4：错误追踪

```python
"""
错误追踪示例
"""
import os
from dotenv import load_dotenv
from langsmith import traceable
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model("groq:llama-3.3-70b-versatile")

@traceable(name="可能失败的操作", tags=["risky"])
def risky_operation(data: str) -> dict:
    """可能失败的操作，错误会被记录"""
    try:
        # 模拟可能失败的操作
        if not data:
            raise ValueError("输入数据为空")

        response = model.invoke([{"role": "user", "content": data}])
        return {"status": "success", "result": response.content}

    except ValueError as e:
        return {"status": "error", "error_type": "validation", "error": str(e)}
    except Exception as e:
        return {"status": "error", "error_type": "unknown", "error": str(e)}

# 测试
result1 = risky_operation("正常输入")
print(f"结果1: {result1}")

result2 = risky_operation("")  # 会触发错误
print(f"结果2: {result2}")

# 在 LangSmith 中可以看到：
# - 成功的调用标记为 "success"
# - 失败的调用标记为 "error"，包含错误详情
```

---

## 常见错误

### 1. 未设置 LANGSMITH_TRACING

```python
# 错误：追踪未启用
os.environ["LANGSMITH_API_KEY"] = "xxx"
# 忘记设置 LANGSMITH_TRACING=true
# 调用不会被记录

# 正确：确保两个都设置
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "xxx"
```

### 2. API Key 无效

```python
# 错误：使用了过期或无效的 API Key
# AuthenticationError: Invalid API key

# 正确：
# 1. 检查 .env 文件中的 Key 是否正确
# 2. 确认 Key 没有过期
# 3. 确认 Key 有正确的权限
```

### 3. 项目名错误

```python
# 错误：项目名不存在
os.environ["LANGSMITH_PROJECT"] = "NonExistentProject"

# 正确：使用已存在的项目名，或让 LangSmith 自动创建
os.environ["LANGSMITH_PROJECT"] = "MyProject"
```

### 4. 追踪装饰器使用不当

```python
# 错误：在异步函数中使用同步 traceable
@traceable
async def async_func():  # 可能有问题
    pass

# 正确：异步函数使用 atraceable 或确保兼容
from langsmith import traceable

@traceable
async def async_func():  # langsmith 支持异步
    pass
```

---

## 最佳实践

### 1. 为所有关键函数添加追踪

```python
# 好：所有关键步骤都有追踪
@traceable(name="数据预处理")
def preprocess(data): ...

@traceable(name="LLM 调用")
def call_llm(prompt): ...

@traceable(name="后处理")
def postprocess(result): ...

# 不好：只追踪了部分函数
def preprocess(data): ...  # 没有追踪
@traceable
def call_llm(prompt): ...
def postprocess(result): ...  # 没有追踪
```

### 2. 使用有意义的 run_name 和 tags

```python
# 好：描述性的名称和标签
@traceable(
    name="用户问题回答",
    tags=["qa", "production", "v2"]
)
def answer(question): ...

# 不好：无意义的名称
@traceable(name="func1")
def answer(question): ...
```

### 3. 在 metadata 中记录业务上下文

```python
config = RunnableConfig(
    metadata={
        "user_id": user_id,
        "session_id": session_id,
        "feature": "chat",
        "experiment": "prompt_v3",
        "model": "gpt-4o",
    }
)
```

### 4. 定期审查 Trace 数据

```
定期检查：
1. 平均响应时间是否有变化
2. Token 消耗是否合理
3. 错误率是否升高
4. 哪些功能使用最多
5. 是否有性能瓶颈
```

---

## 练习题

### 练习1：基础追踪

为一个简单的问答函数添加 LangSmith 追踪：
1. 设置环境变量
2. 使用 @traceable 装饰器
3. 在 LangSmith UI 中查看追踪结果

```python
# 在此编写你的代码
```

### 练习2：嵌套追踪

创建一个多步骤的处理流程，每个步骤都使用 @traceable：
1. 预处理步骤
2. LLM 分析步骤
3. 后处理步骤
4. 查看嵌套的追踪结构

```python
# 在此编写你的代码
```

### 练习3：性能分析

使用 LangSmith 追踪一个批量处理任务：
1. 处理 10 个问题
2. 在 LangSmith 中分析总耗时
3. 找到最慢的调用
4. 计算平均 token 消耗

```python
# 在此编写你的代码
```

---

**相关章节**：
- [23-错误处理](./23-错误处理.md) - 错误处理最佳实践
- [16-LangGraph基础](./16-LangGraph基础.md) - LangGraph 基础
