# 15 - 高级工具与 Agent 模式（Advanced Tools & Agent Patterns）

## 目录

1. [Pydantic args_schema 工具参数验证](#1-pydantic-args_schema-工具参数验证)
2. [异步工具](#2-异步工具)
3. [StructuredTool.from_function()](#3-structuredtoolfrom_function)
4. [BaseCallbackHandler 监控](#4-basecallbackhandler-监控)
5. [工具组合模式](#5-工具组合模式)
6. [生产级 Agent 配置](#6-生产级-agent-配置)
7. [完整代码示例](#7-完整代码示例)
8. [常见错误](#8-常见错误)
9. [最佳实践](#9-最佳实践)
10. [练习题](#10-练习题)

---

## 1. Pydantic args_schema 工具参数验证

### 定义参数模型

```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool


class SearchInput(BaseModel):
    """搜索参数模型"""
    query: str = Field(description="搜索关键词")
    max_results: int = Field(
        default=10,
        description="最大结果数",
        ge=1,
        le=100
    )
    language: str = Field(
        default="zh",
        description="语言：zh/en"
    )


@tool(args_schema=SearchInput)
def search_documents(query: str, max_results: int = 10, language: str = "zh") -> str:
    """
    搜索文档

    根据关键词搜索相关文档，支持中文和英文。
    """
    # 工具实现
    results = [f"文档{i}: 关于{query}的内容..." for i in range(max_results)]
    return "\n".join(results)
```

### 复杂参数类型

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from langchain_core.tools import tool


class Priority(str, Enum):
    """优先级枚举"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskInput(BaseModel):
    """任务参数模型"""
    title: str = Field(description="任务标题", min_length=1, max_length=100)
    description: str = Field(description="任务描述")
    priority: Priority = Field(description="任务优先级")
    tags: List[str] = Field(description="标签列表", min_length=1, max_length=5)
    assignee: Optional[str] = Field(default=None, description="负责人")
    metadata: Optional[Dict[str, str]] = Field(
        default=None,
        description="额外元数据"
    )


@tool(args_schema=TaskInput)
def create_task(
    title: str,
    description: str,
    priority: Priority,
    tags: List[str],
    assignee: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None
) -> str:
    """
    创建任务

    创建一个新的任务，包含标题、描述、优先级等信息。
    """
    task = {
        "title": title,
        "description": description,
        "priority": priority.value,
        "tags": tags,
        "assignee": assignee,
        "metadata": metadata
    }

    return f"任务创建成功: {task}"
```

### 参数验证示例

```python
from pydantic import BaseModel, Field, field_validator
from langchain_core.tools import tool


class EmailInput(BaseModel):
    """邮件参数模型"""
    to: str = Field(description="收件人邮箱")
    subject: str = Field(description="邮件主题", min_length=1, max_length=200)
    body: str = Field(description="邮件内容")
    cc: Optional[List[str]] = Field(default=None, description="抄送列表")

    @field_validator("to")
    @classmethod
    def validate_email(cls, v):
        """验证邮箱格式"""
        import re
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError(f"邮箱格式不正确: {v}")
        return v

    @field_validator("cc")
    @classmethod
    def validate_cc_list(cls, v):
        """验证抄送列表"""
        if v is not None:
            import re
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            for email in v:
                if not re.match(pattern, email):
                    raise ValueError(f"抄送邮箱格式不正确: {email}")
        return v


@tool(args_schema=EmailInput)
def send_email(
    to: str,
    subject: str,
    body: str,
    cc: Optional[List[str]] = None
) -> str:
    """
    发送邮件

    发送一封邮件到指定收件人，支持抄送功能。
    """
    # 模拟发送邮件
    return f"邮件已发送到 {to}，主题: {subject}"
```

---

## 2. 异步工具

### async def 定义异步工具

```python
import asyncio
from langchain_core.tools import tool
import aiohttp


@tool
async def fetch_weather_async(city: str) -> str:
    """
    异步获取天气信息

    参数:
        city: 城市名称

    返回:
        天气信息字符串
    """
    # 模拟异步API调用
    await asyncio.sleep(0.1)  # 模拟网络延迟

    weather_data = {
        "北京": "晴天，25°C",
        "上海": "多云，22°C",
        "广州": "阵雨，28°C",
    }

    return weather_data.get(city, f"未找到{city}的天气信息")


@tool
async def search_web_async(query: str) -> str:
    """
    异步网络搜索

    参数:
        query: 搜索查询

    返回:
        搜索结果
    """
    # 使用aiohttp进行异步HTTP请求
    async with aiohttp.ClientSession() as session:
        # 模拟搜索API
        await asyncio.sleep(0.2)
        return f"搜索 '{query}' 的结果: [模拟结果...]"
```

### 适用于 IO 密集型任务

```
┌─────────────────────────────────────────────────────────────┐
│              异步工具适用场景                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  适合异步的任务（IO密集型）:                                   │
│  - 网络请求（API调用、网页抓取）                              │
│  - 文件读写                                                  │
│  - 数据库查询                                                │
│  - 外部服务调用                                               │
│                                                             │
│  不适合异步的任务（CPU密集型）:                                │
│  - 复杂计算                                                  │
│  - 数据处理                                                  │
│  - 图像处理                                                  │
│                                                             │
│  示例:                                                      │
│  同步版本: 3个API调用串行执行 = 3秒                           │
│  异步版本: 3个API调用并行执行 = 1秒                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 同步 vs 异步工具对比

```python
"""
同步 vs 异步工具对比
"""
import asyncio
import time
from langchain_core.tools import tool


# 同步工具
@tool
def sync_fetch_data(url: str) -> str:
    """同步获取数据"""
    import requests
    time.sleep(1)  # 模拟网络延迟
    return f"从 {url} 获取的数据"


# 异步工具
@tool
async def async_fetch_data(url: str) -> str:
    """异步获取数据"""
    import aiohttp
    await asyncio.sleep(1)  # 模拟网络延迟
    return f"从 {url} 获取的数据"


async def compare_sync_async():
    """对比同步和异步执行"""

    urls = ["http://api1.com", "http://api2.com", "http://api3.com"]

    # 同步执行（串行）
    start = time.time()
    for url in urls:
        sync_fetch_data.invoke({"url": url})
    sync_time = time.time() - start

    # 异步执行（并行）
    start = time.time()
    tasks = [async_fetch_data.ainvoke({"url": url}) for url in urls]
    await asyncio.gather(*tasks)
    async_time = time.time() - start

    print(f"同步执行时间: {sync_time:.2f}秒")
    print(f"异步执行时间: {async_time:.2f}秒")
    print(f"性能提升: {sync_time / async_time:.2f}x")


if __name__ == "__main__":
    asyncio.run(compare_sync_async())
```

---

## 3. StructuredTool.from_function()

### 更精细的工具控制

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Optional


class CalculatorInput(BaseModel):
    """计算器参数"""
    expression: str = Field(description="数学表达式，例如: 2+3*4")
    precision: int = Field(
        default=2,
        description="小数精度",
        ge=0,
        le=10
    )


def calculator_func(expression: str, precision: int = 2) -> str:
    """计算器函数实现"""
    try:
        result = eval(expression)
        return f"{result:.{precision}f}"
    except Exception as e:
        return f"计算错误: {e}"


# 使用StructuredTool创建工具
calculator_tool = StructuredTool.from_function(
    func=calculator_func,
    name="calculator",
    description="执行数学计算，支持基本运算（+, -, *, /）",
    args_schema=CalculatorInput,
    return_direct=False,  # 是否直接返回给用户
)
```

### 自定义名称、描述、参数模式

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional


class SearchInput(BaseModel):
    """搜索参数"""
    query: str = Field(description="搜索关键词")
    filters: Optional[List[str]] = Field(
        default=None,
        description="过滤条件"
    )


def advanced_search(query: str, filters: Optional[List[str]] = None) -> str:
    """高级搜索实现"""
    result = f"搜索 '{query}'"
    if filters:
        result += f"，过滤: {', '.join(filters)}"
    return result


# 创建高级工具
search_tool = StructuredTool.from_function(
    func=advanced_search,
    name="advanced_search",
    description="""
    高级搜索工具

    支持关键词搜索和过滤条件。
    - query: 搜索关键词（必填）
    - filters: 过滤条件列表（可选）

    示例: advanced_search(query="Python", filters=["教程", "入门"])
    """,
    args_schema=SearchInput,
    return_direct=False,
    verbose=True,  # 显示详细信息
)
```

### StructuredTool vs @tool 装饰器

```python
"""
StructuredTool vs @tool 装饰器对比
"""
from langchain_core.tools import StructuredTool, tool
from pydantic import BaseModel, Field


# 方式1: @tool装饰器（简单）
@tool
def simple_calculator(expression: str) -> str:
    """计算数学表达式"""
    return str(eval(expression))


# 方式2: StructuredTool.from_function()（灵活）
class CalcInput(BaseModel):
    expression: str = Field(description="数学表达式")
    precision: int = Field(default=2, description="精度")


def calc_func(expression: str, precision: int = 2) -> str:
    return f"{eval(expression):.{precision}f}"


advanced_calculator = StructuredTool.from_function(
    func=calc_func,
    name="advanced_calculator",
    description="高级计算器，支持精度控制",
    args_schema=CalcInput,
    return_direct=False,
)


# 对比:
# @tool: 简单快速，适合简单工具
# StructuredTool: 更灵活，支持自定义名称、描述、参数验证
```

---

## 4. BaseCallbackHandler 监控

### on_tool_start / on_tool_end / on_tool_error

```python
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List, Optional
from langchain_core.messages import BaseMessage


class ToolMonitorHandler(BaseCallbackHandler):
    """工具监控Handler"""

    def __init__(self):
        self.tool_calls = []
        self.errors = []

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: Any = None,
        parent_run_id: Any = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        inputs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """工具开始执行时调用"""
        tool_name = serialized.get("name", "unknown")
        print(f"[Tool Start] {tool_name}")
        print(f"  输入: {input_str[:100]}...")

        self.tool_calls.append({
            "tool": tool_name,
            "input": input_str,
            "start_time": __import__('time').time(),
            "status": "running"
        })

    def on_tool_end(
        self,
        output: str,
        *,
        run_id: Any = None,
        parent_run_id: Any = None,
        **kwargs: Any,
    ) -> None:
        """工具执行完成时调用"""
        if self.tool_calls:
            last_call = self.tool_calls[-1]
            last_call["status"] = "success"
            last_call["output"] = output[:200]
            last_call["end_time"] = __import__('time').time()
            last_call["duration"] = last_call["end_time"] - last_call["start_time"]

            print(f"[Tool End] 成功")
            print(f"  耗时: {last_call['duration']:.2f}秒")
            print(f"  输出: {output[:100]}...")

    def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: Any = None,
        parent_run_id: Any = None,
        **kwargs: Any,
    ) -> None:
        """工具执行出错时调用"""
        if self.tool_calls:
            last_call = self.tool_calls[-1]
            last_call["status"] = "error"
            last_call["error"] = str(error)
            last_call["end_time"] = __import__('time').time()

        self.errors.append({
            "tool": last_call.get("tool", "unknown"),
            "error": str(error),
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })

        print(f"[Tool Error] {error}")

    def get_stats(self) -> Dict:
        """获取统计信息"""
        total_calls = len(self.tool_calls)
        successful = sum(1 for c in self.tool_calls if c["status"] == "success")
        failed = sum(1 for c in self.tool_calls if c["status"] == "error")

        durations = [
            c.get("duration", 0)
            for c in self.tool_calls
            if "duration" in c
        ]

        return {
            "total_calls": total_calls,
            "successful": successful,
            "failed": failed,
            "avg_duration": sum(durations) / len(durations) if durations else 0,
            "errors": self.errors
        }
```

### 自定义监控 Handler

```python
"""
自定义监控Handler示例
"""
from langchain_core.callbacks import BaseCallbackHandler
from collections import defaultdict
from datetime import datetime
import json


class DetailedMonitorHandler(BaseCallbackHandler):
    """详细监控Handler"""

    def __init__(self, log_file: str = "tool_monitor.log"):
        self.log_file = log_file
        self.stats = defaultdict(lambda: {
            "calls": 0,
            "successes": 0,
            "errors": 0,
            "total_duration": 0
        })
        self.current_calls = {}

    def _log(self, message: str):
        """写入日志"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "unknown")
        run_id = kwargs.get("run_id")

        self.current_calls[run_id] = {
            "tool": tool_name,
            "start_time": __import__('time').time()
        }

        self.stats[tool_name]["calls"] += 1

        self._log(f"TOOL_START | {tool_name} | input={input_str[:100]}")

    def on_tool_end(self, output, **kwargs):
        run_id = kwargs.get("run_id")

        if run_id in self.current_calls:
            call = self.current_calls[run_id]
            duration = __import__('time').time() - call["start_time"]

            self.stats[call["tool"]]["successes"] += 1
            self.stats[call["tool"]]["total_duration"] += duration

            self._log(
                f"TOOL_END | {call['tool']} | "
                f"duration={duration:.2f}s | output={output[:100]}"
            )

            del self.current_calls[run_id]

    def on_tool_error(self, error, **kwargs):
        run_id = kwargs.get("run_id")

        if run_id in self.current_calls:
            call = self.current_calls[run_id]

            self.stats[call["tool"]]["errors"] += 1

            self._log(
                f"TOOL_ERROR | {call['tool']} | error={str(error)}"
            )

            del self.current_calls[run_id]

    def get_report(self) -> str:
        """生成监控报告"""
        report = "=" * 50 + "\n"
        report += "工具监控报告\n"
        report += "=" * 50 + "\n\n"

        for tool_name, stats in self.stats.items():
            avg_duration = (
                stats["total_duration"] / stats["successes"]
                if stats["successes"] > 0
                else 0
            )

            report += f"工具: {tool_name}\n"
            report += f"  调用次数: {stats['calls']}\n"
            report += f"  成功次数: {stats['successes']}\n"
            report += f"  失败次数: {stats['errors']}\n"
            report += f"  平均耗时: {avg_duration:.2f}秒\n\n"

        return report
```

---

## 5. 工具组合模式

### 工具链

```python
"""
工具链示例：多个工具串行执行
"""
from langchain_core.tools import tool
from typing import List


@tool
def extract_keywords(text: str) -> List[str]:
    """从文本中提取关键词"""
    # 简单实现：按空格分词
    keywords = text.split()[:5]
    return keywords


@tool
def search_documents(keywords: List[str]) -> str:
    """根据关键词搜索文档"""
    query = " ".join(keywords)
    return f"搜索 '{query}' 的结果: [文档列表...]"


@tool
def summarize_document(document: str) -> str:
    """总结文档内容"""
    return f"文档摘要: {document[:100]}..."


# 工具链执行
def tool_chain_example():
    """工具链示例"""
    from langchain.chat_models import init_chat_model
    from langchain.agents import create_agent

    model = init_chat_model("groq:llama-3.3-70b-versatile")

    agent = create_agent(
        model=model,
        tools=[extract_keywords, search_documents, summarize_document],
        system_prompt="""你是一个文档分析助手。

分析流程：
1. 使用extract_keywords从用户输入中提取关键词
2. 使用search_documents根据关键词搜索相关文档
3. 使用summarize_document总结找到的文档

按照这个顺序执行工具。"""
    )

    return agent
```

### 工具并行

```python
"""
工具并行执行示例
"""
import asyncio
from langchain_core.tools import tool


@tool
async def fetch_weather(city: str) -> str:
    """获取天气"""
    await asyncio.sleep(1)  # 模拟API调用
    return f"{city}: 晴天，25°C"


@tool
async def fetch_news(topic: str) -> str:
    """获取新闻"""
    await asyncio.sleep(1)  # 模拟API调用
    return f"{topic}新闻: [新闻内容...]"


@tool
async def fetch_stocks(symbol: str) -> str:
    """获取股票信息"""
    await asyncio.sleep(1)  # 模拟API调用
    return f"{symbol}: $150.25"


async def parallel_execution():
    """并行执行多个工具"""

    # 并行调用多个工具
    results = await asyncio.gather(
        fetch_weather.ainvoke({"city": "北京"}),
        fetch_news.ainvoke({"topic": "科技"}),
        fetch_stocks.ainvoke({"symbol": "AAPL"})
    )

    for result in results:
        print(result)


if __name__ == "__main__":
    asyncio.run(parallel_execution())
```

---

## 6. 生产级 Agent 配置

### 错误恢复

```python
"""
生产级Agent错误恢复配置
"""
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import AgentMiddleware
from typing import Any, List, Optional
from langchain_core.messages import BaseMessage


class ErrorRecoveryMiddleware(AgentMiddleware):
    """错误恢复中间件"""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.retry_count = 0

    async def before_model(self, messages: List[BaseMessage], **kwargs):
        return None

    async def after_model(self, messages, response, **kwargs):
        # 检查是否有工具调用错误
        if hasattr(response, 'tool_calls'):
            for tc in response.tool_calls:
                if tc.get("error"):
                    self.retry_count += 1
                    if self.retry_count > self.max_retries:
                        raise Exception("超过最大重试次数")
        return response


@tool
def risky_operation(data: str) -> str:
    """可能失败的操作"""
    import random
    if random.random() < 0.3:  # 30%概率失败
        raise ValueError("操作失败")
    return f"处理结果: {data}"


def create_production_agent():
    """创建生产级Agent"""

    model = init_chat_model("groq:llama-3.3-70b-versatile")

    # 配置重试
    model_with_retry = model.with_retry(
        stop_after_attempt=3,
        wait_exponential=True
    )

    # 配置降级
    fallback_model = init_chat_model("groq:llama-3.1-8b-instant")
    model_with_fallback = model_with_retry.with_fallbacks([fallback_model])

    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model_with_fallback,
        tools=[risky_operation],
        system_prompt="你是一个助手，使用工具完成任务。",
        checkpointer=checkpointer,
        middleware=[ErrorRecoveryMiddleware(max_retries=3)]
    )

    return agent
```

### 超时控制

```python
"""
超时控制示例
"""
import asyncio
from langchain_core.tools import tool
from concurrent.futures import TimeoutError


@tool
async def slow_operation(data: str) -> str:
    """耗时操作"""
    await asyncio.sleep(10)  # 模拟长时间操作
    return f"处理完成: {data}"


async def execute_with_timeout(tool_func, inputs: dict, timeout: float = 5.0):
    """带超时的工具执行"""
    try:
        result = await asyncio.wait_for(
            tool_func.ainvoke(inputs),
            timeout=timeout
        )
        return result
    except TimeoutError:
        return f"操作超时（{timeout}秒）"
    except Exception as e:
        return f"操作失败: {e}"


async def timeout_example():
    """超时控制示例"""

    result = await execute_with_timeout(
        slow_operation,
        {"data": "测试数据"},
        timeout=3.0
    )
    print(result)  # 输出: 操作超时（3.0秒）


if __name__ == "__main__":
    asyncio.run(timeout_example())
```

---

## 7. 完整代码示例

### 示例1：完整的生产级 Agent 系统

```python
"""
完整的生产级Agent系统
"""
import time
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import defaultdict

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_core.tools import tool, StructuredTool
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver


# ==================== 监控Handler ====================
class ProductionMonitorHandler(BaseCallbackHandler):
    """生产环境监控Handler"""

    def __init__(self):
        self.metrics = defaultdict(lambda: {
            "calls": 0,
            "successes": 0,
            "errors": 0,
            "total_duration": 0
        })
        self.start_times = {}

    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name", "unknown")
        run_id = kwargs.get("run_id")

        self.start_times[run_id] = time.time()
        self.metrics[tool_name]["calls"] += 1

        print(f"[{datetime.now().isoformat()}] TOOL_START: {tool_name}")

    def on_tool_end(self, output, **kwargs):
        run_id = kwargs.get("run_id")

        if run_id in self.start_times:
            duration = time.time() - self.start_times[run_id]
            # 找到对应的工具名
            for tool_name, stats in self.metrics.items():
                if stats["calls"] > stats["successes"] + stats["errors"]:
                    stats["successes"] += 1
                    stats["total_duration"] += duration
                    break

            print(f"[{datetime.now().isoformat()}] TOOL_END: {duration:.2f}s")
            del self.start_times[run_id]

    def on_tool_error(self, error, **kwargs):
        run_id = kwargs.get("run_id")

        if run_id in self.start_times:
            for tool_name, stats in self.metrics.items():
                if stats["calls"] > stats["successes"] + stats["errors"]:
                    stats["errors"] += 1
                    break

            print(f"[{datetime.now().isoformat()}] TOOL_ERROR: {error}")
            del self.start_times[run_id]

    def get_report(self) -> str:
        report = "监控报告:\n"
        for tool_name, stats in self.metrics.items():
            avg = stats["total_duration"] / stats["successes"] if stats["successes"] > 0 else 0
            report += f"  {tool_name}: {stats['calls']}次调用, "
            report += f"{stats['successes']}次成功, "
            report += f"{stats['errors']}次失败, "
            report += f"平均{avg:.2f}秒\n"
        return report


# ==================== 中间件 ====================
class RateLimitMiddleware(AgentMiddleware):
    """限流中间件"""

    def __init__(self, max_calls_per_minute: int = 10):
        self.max_calls = max_calls_per_minute
        self.call_times = []

    async def before_model(self, messages: List[BaseMessage], **kwargs):
        now = time.time()

        # 清理过期记录
        self.call_times = [t for t in self.call_times if now - t < 60]

        # 检查限流
        if len(self.call_times) >= self.max_calls:
            raise Exception(f"超过限流: {self.max_calls}次/分钟")

        self.call_times.append(now)
        return None

    async def after_model(self, messages, response, **kwargs):
        return None


# ==================== 工具定义 ====================
class DatabaseQueryInput(BaseModel):
    """数据库查询参数"""
    table: str = Field(description="表名")
    conditions: Optional[Dict[str, Any]] = Field(
        default=None,
        description="查询条件"
    )
    limit: int = Field(default=10, description="返回数量限制", ge=1, le=100)


@tool(args_schema=DatabaseQueryInput)
def query_database(
    table: str,
    conditions: Optional[Dict[str, Any]] = None,
    limit: int = 10
) -> str:
    """
    查询数据库

    从指定表中查询数据，支持条件过滤和数量限制。
    """
    # 模拟数据库查询
    results = [
        {"id": i, "name": f"记录{i}", "table": table}
        for i in range(min(limit, 5))
    ]

    return f"查询到 {len(results)} 条记录: {results}"


@tool
def send_notification(message: str, channel: str = "default") -> str:
    """
    发送通知

    通过指定渠道发送通知消息。
    """
    # 模拟发送通知
    return f"通知已发送到 {channel} 渠道: {message}"


# ==================== 创建生产级Agent ====================
def create_production_agent():
    """创建生产级Agent"""

    # 模型配置
    primary_model = init_chat_model("groq:llama-3.3-70b-versatile")
    fallback_model = init_chat_model("groq:llama-3.1-8b-instant")

    model = (
        primary_model
        .with_retry(stop_after_attempt=3, wait_exponential=True)
        .with_fallbacks([fallback_model])
    )

    # 监控
    monitor = ProductionMonitorHandler()

    # 检查点
    checkpointer = InMemorySaver()

    # 创建Agent
    agent = create_agent(
        model=model,
        tools=[query_database, send_notification],
        system_prompt="""你是生产环境助手。

可用工具：
1. query_database: 查询数据库
2. send_notification: 发送通知

使用规范：
- 先查询数据，再发送通知
- 限制查询结果数量
- 记录所有操作""",
        checkpointer=checkpointer,
        middleware=[
            RateLimitMiddleware(max_calls_per_minute=20),
        ],
        callbacks=[monitor]
    )

    return agent, monitor


def main():
    """主函数"""
    agent, monitor = create_production_agent()

    config = {"configurable": {"thread_id": "production"}}

    # 测试调用
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "查询用户表的前5条记录"}]},
        config=config
    )

    print(f"\n回答: {response['messages'][-1].content}")
    print(f"\n{monitor.get_report()}")


if __name__ == "__main__":
    main()
```

### 示例2：异步工具Agent

```python
"""
异步工具Agent示例
"""
import asyncio
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
async def fetch_data_from_api(endpoint: str) -> str:
    """从API获取数据"""
    await asyncio.sleep(0.5)  # 模拟API调用
    return f"来自 {endpoint} 的数据: [模拟数据]"


@tool
async def process_data(data: str) -> str:
    """处理数据"""
    await asyncio.sleep(0.3)  # 模拟处理
    return f"处理结果: {data[:50]}..."


@tool
async def save_results(results: str, filename: str) -> str:
    """保存结果到文件"""
    await asyncio.sleep(0.2)  # 模拟文件写入
    return f"结果已保存到 {filename}"


async def async_agent_example():
    """异步Agent示例"""

    model = init_chat_model("groq:llama-3.3-70b-versatile")
    checkpointer = InMemorySaver()

    agent = create_agent(
        model=model,
        tools=[fetch_data_from_api, process_data, save_results],
        system_prompt="你是一个数据处理助手，使用工具完成数据处理流程。",
        checkpointer=checkpointer
    )

    config = {"configurable": {"thread_id": "async-demo"}}

    # 异步调用Agent
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "从API获取数据并处理保存"}]},
        config=config
    )

    print(f"回答: {response['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(async_agent_example())
```

---

## 8. 常见错误

### 错误1：异步工具在同步上下文中调用

```python
# 错误：在同步代码中直接调用异步工具
@tool
async def async_tool(input: str) -> str:
    return f"结果: {input}"

# 这样会返回协程对象，而不是结果
result = async_tool.invoke({"input": "test"})  # 错误

# 正确：使用ainvoke
result = await async_tool.ainvoke({"input": "test"})

# 或者在异步上下文中
async def main():
    result = await async_tool.ainvoke({"input": "test"})
```

### 错误2：args_schema 与函数参数不匹配

```python
# 错误：args_schema定义的字段与函数参数不一致
class Input(BaseModel):
    query: str
    limit: int

@tool(args_schema=Input)
def search(query: str, max_results: int):  # 参数名不一致
    pass

# 正确：保持一致
class Input(BaseModel):
    query: str
    max_results: int

@tool(args_schema=Input)
def search(query: str, max_results: int):
    pass
```

### 错误3：监控Handler未正确处理run_id

```python
# 错误：未使用run_id关联开始和结束事件
class BadHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        self.current_tool = serialized["name"]  # 可能被并发调用覆盖

# 正确：使用run_id关联
class GoodHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        run_id = kwargs.get("run_id")
        self.calls[run_id] = {"tool": serialized["name"]}

    def on_tool_end(self, output, **kwargs):
        run_id = kwargs.get("run_id")
        if run_id in self.calls:
            # 处理对应的调用
            pass
```

### 错误4：工具链顺序错误

```python
# 错误：工具链中后续工具依赖前序工具的结果，但未确保顺序
agent = create_agent(
    model=model,
    tools=[process_data, extract_keywords],  # 顺序错误
    system_prompt="先提取关键词，再处理数据"
)

# 正确：按执行顺序排列工具
agent = create_agent(
    model=model,
    tools=[extract_keywords, process_data],  # 正确顺序
    system_prompt="先提取关键词，再处理数据"
)
```

---

## 9. 最佳实践

### 1. 使用 args_schema 进行参数验证

```python
# 好：使用Pydantic验证参数
class Input(BaseModel):
    email: str = Field(description="邮箱")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("邮箱格式不正确")
        return v

@tool(args_schema=Input)
def send_email(email: str):
    pass
```

### 2. 为IO密集型任务使用异步工具

```python
# 网络请求、文件IO等使用异步
@tool
async def fetch_api(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()
```

### 3. 实现监控和日志

```python
class MonitorHandler(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        logger.info(f"Tool started: {serialized['name']}")

    def on_tool_end(self, output, **kwargs):
        logger.info(f"Tool completed")

    def on_tool_error(self, error, **kwargs):
        logger.error(f"Tool error: {error}")
```

### 4. 配置超时和重试

```python
model = (
    init_chat_model("groq:llama-3.3-70b-versatile")
    .with_retry(stop_after_attempt=3)
    .with_fallbacks([backup_model])
)
```

---

## 10. 练习题

### 练习1：参数验证工具

创建一个带Pydantic参数验证的工具：
1. 定义复杂的参数模型
2. 实现自定义验证器
3. 测试各种边界情况

### 练习2：异步工具

实现异步工具：
1. 创建至少3个异步工具
2. 实现并行执行
3. 比较同步和异步的性能差异

### 练习3：监控系统

实现一个完整的监控系统：
1. 创建自定义CallbackHandler
2. 记录工具调用的详细信息
3. 生成监控报告

### 练习4：生产级Agent

构建一个生产级Agent系统：
1. 实现错误恢复机制
2. 配置超时控制
3. 添加限流中间件
4. 集成监控系统
5. 测试各种异常场景

---

[上一章：14-RAG进阶](./14-RAG进阶.md) | [返回目录](#目录)
