# 25 - 项目实战：多 Agent 客服系统

## 目录

- [项目概述](#项目概述)
- [系统架构](#系统架构)
- [环境准备](#环境准备)
- [核心组件实现](#核心组件实现)
  - [意图分类器](#1-意图分类器)
  - [专业 Agent](#2-专业-agent)
  - [路由系统](#3-路由系统)
  - [质量检查](#4-质量检查)
  - [人工升级](#5-人工升级)
- [LangGraph 图定义](#langgraph-图定义)
- [完整项目代码](#完整项目代码)
- [测试场景](#测试场景)
- [常见错误](#常见错误)
- [最佳实践](#最佳实践)
- [练习题](#练习题)

---

## 项目概述

在真实的客服场景中，用户的问题涵盖技术支持、订单查询、产品咨询、投诉建议等多个领域。单一 Agent 难以高质量地处理所有类型的问题。多 Agent 系统通过**专业化分工**和**智能路由**，将不同类型的问题分配给最擅长该领域的 Agent 处理。

### 项目目标

构建一个**多 Agent 客户服务系统**，具备以下能力：

1. **智能意图识别**：自动判断用户问题属于哪个类别
2. **专业化处理**：每个领域由专属 Agent 处理，配备专用工具
3. **自动路由**：基于意图自动将请求路由到正确的 Agent
4. **质量保证**：对生成的回答进行质量评估，不合格时自动重新生成
5. **人工升级**：复杂或敏感问题自动转接人工客服

### 设计原则

| 原则 | 说明 |
|------|------|
| 单一职责 | 每个 Agent 只负责一个领域 |
| 松耦合 | Agent 之间通过状态传递信息，不直接调用 |
| 可扩展 | 新增领域只需添加新 Agent 和路由规则 |
| 有状态 | 使用 LangGraph 管理全局对话状态 |

---

## 系统架构

### 整体架构图

```
+================================================================+
|                    多Agent客服系统架构                             |
+================================================================+

    用户消息
       |
       v
+------+-------+
|   意图分类器   |  <--- 结构化输出 (IntentClassification)
| (LLM + Pydantic)|
+------+-------+
       |
       v
+------+-------+
|   路由分发     |  <--- 条件边 (conditional_edges)
+--+---+---+---+
   |   |   |
   v   v   v
+--+--+ +-+-+ +--+--+
|技术 | |订单| |产品 |  <--- 专业 Agent（各自有专用工具）
|支持 | |服务| |咨询 |
+--+--+ +-+-+ +--+--+
   |   |   |
   v   v   v
+------+-------+
|   质量检查     |  <--- 评估回答质量
+------+-------+
       |
   +---+---+
   |       |
 满意     不满意
   |       |
   v       v
+--+--+  +-+----------+
| 输出 |  | 重新生成    |
+-----+  | (带反馈)    |
         +------------+

   复杂/敏感问题
       |
       v
+------+-------+
|   人工升级     |  <--- 自动检测升级条件
+------+-------+
       |
       v
    转接人工
```

### LangGraph 状态流转图

```
+-------+
| START |
+---+---+
    |
    v
+---+-----------+
| classify_intent|  -- 意图分类
+---+-----------+
    |
    v
+---+-----------+
| route_by_intent|  -- 条件路由
+---+---+---+---+
    |   |   |
    v   v   v
+---+-+ +--++ +---+-+
|tech_| |ord_| |prod_|
|supp | |svc | |inqu |
+---+-+ +--++ +---+-+
    |   |   |
    v   v   v
+---+-----------+
| quality_check  |  -- 质量评估
+---+-----------+
    |
    +-------+-------+
    |               |
    v               v
+---+---+     +----+------+
|  END  |     | regenerate |
+-------+     +----+------+
                   |
                   v
              +----+------+
              |quality_chk| (循环回质量检查)
              +-----------+

   特殊路径：
   classify_intent --> human_escalation --> END
```

---

## 环境准备

### 依赖安装

```bash
pip install langchain>=1.0.0 langgraph>=1.0.0 langchain-core>=1.0.0
pip install langchain-groq
pip install pydantic>=2.0
```

### 环境变量

```bash
# .env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 核心组件实现

### 1. 意图分类器

意图分类器使用 LLM 的结构化输出能力，将用户消息分类为预定义的类别。

```python
"""意图分类器 - 基于结构化输出的智能分类"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage


# ========== 意图定义 ==========
class IntentType(str, Enum):
    """客户意图类型枚举"""
    TECHNICAL_SUPPORT = "technical_support"   # 技术支持
    ORDER_SERVICE = "order_service"           # 订单服务
    PRODUCT_INQUIRY = "product_inquiry"       # 产品咨询
    COMPLAINT = "complaint"                   # 投诉建议
    GENERAL = "general"                       # 一般咨询
    ESCALATION = "escalation"                 # 需要人工介入


class IntentClassification(BaseModel):
    """意图分类结果（结构化输出）"""
    intent: IntentType = Field(
        description="用户的主要意图类别"
    )
    confidence: float = Field(
        description="分类置信度，0.0 到 1.0 之间",
        ge=0.0, le=1.0,
    )
    reasoning: str = Field(
        description="分类理由，简要说明为什么归为此类别"
    )
    sub_topic: Optional[str] = Field(
        default=None,
        description="子话题，如 '退款', '登录问题', '产品规格' 等"
    )
    requires_escalation: bool = Field(
        default=False,
        description="是否需要升级到人工客服"
    )


# ========== 分类器实现 ==========
INTENT_CLASSIFIER_PROMPT = """你是一个专业的客户服务意图分类器。

根据用户的消息，判断其意图类别，并输出结构化的分类结果。

意图类别说明：
- technical_support: 技术问题，如软件故障、登录问题、错误报告、使用方法
- order_service: 订单相关，如订单查询、物流跟踪、退换货、发票
- product_inquiry: 产品咨询，如功能介绍、价格、规格、对比
- complaint: 投诉建议，如服务不满、质量问题、改进建议
- general: 一般性问候或不明确的咨询
- escalation: 涉及法律、安全、严重投诉等需要人工介入的情况

注意：
1. 如果用户的问题模糊，选择 general 并降低置信度
2. 如果涉及退款金额较大、法律问题、人身安全等，设置 requires_escalation 为 true
3. reasoning 字段用中文填写
"""


async def classify_intent(llm, user_message: str) -> IntentClassification:
    """对用户消息进行意图分类"""
    # 使用结构化输出
    structured_llm = llm.with_structured_output(IntentClassification)

    response = await structured_llm.ainvoke([
        SystemMessage(content=INTENT_CLASSIFIER_PROMPT),
        HumanMessage(content=user_message),
    ])

    return response


# 同步版本
def classify_intent_sync(llm, user_message: str) -> IntentClassification:
    """同步版本的意图分类"""
    structured_llm = llm.with_structured_output(IntentClassification)

    response = structured_llm.invoke([
        SystemMessage(content=INTENT_CLASSIFIER_PROMPT),
        HumanMessage(content=user_message),
    ])

    return response
```

**关键设计点**：
- 使用 Pydantic `BaseModel` 定义输出结构，确保 LLM 返回格式化数据
- `Field` 中的 `description` 会传递给 LLM，帮助其理解每个字段的含义
- `ge` 和 `le` 约束确保数值在合法范围内

### 2. 专业 Agent

每个专业 Agent 都有自己专属的系统提示词和工具集。

```python
"""专业 Agent 定义 - 各领域专属客服"""

from langchain_core.tools import tool


# ========== 技术支持工具 ==========
@tool
def search_knowledge_base(query: str) -> str:
    """搜索技术知识库，查找与用户问题相关的技术文档和解决方案。

    Args:
        query: 搜索关键词或问题描述
    """
    # 实际项目中接入知识库
    kb_results = {
        "登录": "常见登录问题解决方案：1. 清除浏览器缓存 2. 重置密码 3. 检查网络连接",
        "报错": "错误代码排查指南：请提供具体的错误代码，以便精准定位问题",
        "安装": "安装指南：请确认系统版本满足最低要求，然后按步骤操作",
    }

    for key, value in kb_results.items():
        if key in query:
            return value

    return f"未找到与 '{query}' 直接相关的知识库条目。建议用户提交工单获取技术支持。"


@tool
def create_support_ticket(title: str, description: str, priority: str = "medium") -> str:
    """创建技术支持工单。

    Args:
        title: 工单标题
        description: 问题详细描述
        priority: 优先级，可选 low/medium/high/critical
    """
    ticket_id = f"TK-2026-{hash(title) % 10000:04d}"
    return (
        f"工单已创建成功。\n"
        f"工单号: {ticket_id}\n"
        f"标题: {title}\n"
        f"优先级: {priority}\n"
        f"预计响应时间: {'1小时' if priority == 'critical' else '24小时'}"
    )


# ========== 订单服务工具 ==========
@tool
def query_order(order_id: str) -> str:
    """查询订单信息，包括订单状态、物流信息等。

    Args:
        order_id: 订单编号，格式如 ORD-20260501-001
    """
    # 模拟订单数据库
    orders = {
        "ORD-20260501-001": {
            "status": "已发货",
            "product": "LangChain 实战教程",
            "amount": "99.00元",
            "tracking": "SF1234567890",
            "estimated_delivery": "2026-05-08",
        },
        "ORD-20260430-002": {
            "status": "待付款",
            "product": "LangGraph 高级课程",
            "amount": "199.00元",
            "tracking": "未发货",
            "estimated_delivery": "付款后3天内",
        },
    }

    if order_id in orders:
        order = orders[order_id]
        return "\n".join([f"{k}: {v}" for k, v in order.items()])
    else:
        return f"未找到订单 {order_id}，请核实订单号是否正确。"


@tool
def process_refund(order_id: str, reason: str) -> str:
    """处理退款申请。

    Args:
        order_id: 订单编号
        reason: 退款原因
    """
    return (
        f"退款申请已提交。\n"
        f"订单号: {order_id}\n"
        f"原因: {reason}\n"
        f"预计处理时间: 3-5个工作日\n"
        f"退款将原路返回到您的支付账户"
    )


# ========== 产品咨询工具 ==========
@tool
def get_product_info(product_name: str) -> str:
    """获取产品详细信息，包括功能、价格、规格等。

    Args:
        product_name: 产品名称
    """
    products = {
        "基础课程": {
            "价格": "99元",
            "内容": "LangChain 1.0 基础入门，包含22个实战模块",
            "时长": "约20小时",
            "适合": "初学者",
        },
        "高级课程": {
            "价格": "199元",
            "内容": "LangGraph 1.0 高级应用，包含多Agent、RAG等",
            "时长": "约30小时",
            "适合": "有基础的开发者",
        },
        "全套课程": {
            "价格": "249元（优惠50元）",
            "内容": "基础课程 + 高级课程 + 3个完整项目",
            "时长": "约60小时",
            "适合": "系统学习",
        },
    }

    for name, info in products.items():
        if name in product_name or product_name in name:
            return "\n".join([f"{k}: {v}" for k, v in info.items()])

    return f"未找到产品 '{product_name}' 的信息。现有产品：{', '.join(products.keys())}"


@tool
def compare_products(product_a: str, product_b: str) -> str:
    """对比两个产品的差异。

    Args:
        product_a: 产品A名称
        product_b: 产品B名称
    """
    return (
        f"产品对比: {product_a} vs {product_b}\n"
        f"{'=' * 40}\n"
        f"基础课程：适合入门，价格低，内容精简\n"
        f"高级课程：适合进阶，深度覆盖 LangGraph\n"
        f"推荐：如果预算允许，选择全套课程最划算"
    )


# ========== Agent 系统提示词 ==========
TECH_SUPPORT_PROMPT = """你是一位专业的技术支持客服人员。

职责范围：
- 解答软件使用问题
- 排查技术故障
- 提供操作指导
- 必要时创建技术支持工单

工作原则：
1. 耐心倾听用户问题，确认具体症状
2. 先尝试搜索知识库寻找已有解决方案
3. 提供清晰、分步骤的操作指引
4. 如果问题复杂，主动创建工单并告知工单号
5. 确认用户问题是否解决

语言风格：专业、耐心、条理清晰
"""

ORDER_SERVICE_PROMPT = """你是一位专业的订单服务客服人员。

职责范围：
- 查询订单状态和物流信息
- 处理退换货申请
- 解答发票相关问题
- 处理支付问题

工作原则：
1. 主动询问订单号以便查询
2. 及时告知订单最新状态
3. 退换货流程清晰说明
4. 涉及金额较大的退款需提醒用户确认

语言风格：亲切、高效、信息准确
"""

PRODUCT_INQUIRY_PROMPT = """你是一位专业的产品咨询客服人员。

职责范围：
- 介绍产品功能和特点
- 解答价格和优惠信息
- 提供产品对比建议
- 推荐适合的产品方案

工作原则：
1. 了解用户需求后再推荐
2. 客观对比，不贬低竞品
3. 突出产品价值而非价格
4. 提供明确的购买建议

语言风格：热情、专业、有说服力
"""
```

### 3. 路由系统

路由系统是多 Agent 架构的核心，它根据意图分类结果将请求导向正确的 Agent。

```python
"""路由系统 - 基于意图的智能路由"""

from typing import Literal


def route_by_intent(state: dict) -> str:
    """根据意图分类结果决定路由目标

    这是一个条件边函数（conditional edge），LangGraph 会根据
    返回值选择下一个执行的节点。
    """
    # 获取意图分类结果
    classification = state.get("intent_classification")
    if classification is None:
        return "general_agent"

    intent = classification.intent
    requires_escalation = classification.requires_escalation

    # 优先检查是否需要人工升级
    if requires_escalation or intent == "escalation":
        return "human_escalation"

    # 根据意图路由到对应 Agent
    intent_to_agent = {
        "technical_support": "tech_support_agent",
        "order_service": "order_service_agent",
        "product_inquiry": "product_agent",
        "complaint": "tech_support_agent",       # 投诉也由技术支持处理
        "general": "general_agent",
    }

    return intent_to_agent.get(intent, "general_agent")


def should_regenerate(state: dict) -> Literal["regenerate", "output"]:
    """质量检查后决定是否需要重新生成"""
    quality_score = state.get("quality_score", 1.0)
    retry_count = state.get("retry_count", 0)

    # 质量分低于 0.6 且重试次数不超过 2 次
    if quality_score < 0.6 and retry_count < 2:
        return "regenerate"

    return "output"


def check_escalation_needed(state: dict) -> Literal["escalate", "continue"]:
    """检查是否需要升级到人工"""
    classification = state.get("intent_classification")

    if classification and classification.requires_escalation:
        return "escalate"

    # 检查重试次数过多的情况
    if state.get("retry_count", 0) >= 2:
        return "escalate"

    return "continue"
```

### 4. 质量检查

```python
"""质量检查模块 - 评估回答质量"""

from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage, HumanMessage


class QualityAssessment(BaseModel):
    """回答质量评估结果"""
    score: float = Field(
        description="质量评分，0.0 到 1.0",
        ge=0.0, le=1.0,
    )
    is_satisfactory: bool = Field(
        description="是否达到质量标准"
    )
    feedback: str = Field(
        description="具体的改进建议"
    )
    issues: list[str] = Field(
        default_factory=list,
        description="发现的问题列表"
    )


QUALITY_CHECK_PROMPT = """你是一个客服回答质量评估专家。

请评估以下客服回答的质量，考虑以下维度：
1. 准确性：回答是否正确、无误导信息
2. 完整性：是否完整回答了用户问题
3. 礼貌性：语气是否专业、友好
4. 实用性：用户是否能根据回答采取行动
5. 简洁性：是否简明扼要，不啰嗦

评分标准：
- 0.8-1.0: 优秀，可以直接发送
- 0.6-0.8: 合格，但有改进空间
- 0.0-0.6: 不合格，需要重新生成
"""


async def check_quality(llm, user_message: str, ai_response: str) -> QualityAssessment:
    """评估回答质量"""
    structured_llm = llm.with_structured_output(QualityAssessment)

    result = await structured_llm.ainvoke([
        SystemMessage(content=QUALITY_CHECK_PROMPT),
        HumanMessage(content=(
            f"用户问题: {user_message}\n\n"
            f"客服回答: {ai_response}\n\n"
            f"请评估上述回答的质量。"
        )),
    ])

    return result
```

### 5. 人工升级

```python
"""人工升级模块 - 复杂问题自动转接"""

from pydantic import BaseModel, Field
from typing import Optional


class EscalationResult(BaseModel):
    """人工升级结果"""
    ticket_id: str = Field(description="升级工单号")
    priority: str = Field(description="优先级")
    summary: str = Field(description="问题摘要")
    reason: str = Field(description="升级原因")
    suggested_department: str = Field(description="建议接单部门")


def create_escalation(
    user_message: str,
    conversation_history: list,
    classification,
) -> EscalationResult:
    """创建人工升级工单"""
    ticket_id = f"ESC-2026-{hash(user_message) % 10000:04d}"

    # 根据意图决定优先级和部门
    priority_map = {
        "complaint": "high",
        "technical_support": "medium",
        "order_service": "medium",
        "product_inquiry": "low",
    }

    department_map = {
        "technical_support": "技术支持部",
        "order_service": "订单服务部",
        "product_inquiry": "产品部",
        "complaint": "客户关系部",
    }

    intent = classification.intent if classification else "general"

    result = EscalationResult(
        ticket_id=ticket_id,
        priority=priority_map.get(intent, "medium"),
        summary=user_message[:100],
        reason=classification.reasoning if classification else "多次重试未成功",
        suggested_department=department_map.get(intent, "客户服务部"),
    )

    return result


def format_escalation_message(result: EscalationResult) -> str:
    """格式化升级消息给用户"""
    return (
        f"非常抱歉，您的问题需要专业人员为您处理。\n\n"
        f"工单号: {result.ticket_id}\n"
        f"优先级: {result.priority}\n"
        f"已转接至: {result.suggested_department}\n"
        f"问题摘要: {result.summary}\n\n"
        f"我们的客服代表将在{'1小时' if result.priority == 'high' else '24小时'}内"
        f"与您联系。感谢您的耐心等待。"
    )
```

---

## LangGraph 图定义

将所有组件组装成完整的 LangGraph 工作流。

```python
"""LangGraph 图定义 - 多Agent客服工作流"""

from typing import Annotated, TypedDict, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


# ========== 状态定义 ==========
class CustomerServiceState(TypedDict):
    """客服系统全局状态"""
    # 消息历史
    messages: Annotated[list[BaseMessage], add_messages]

    # 意图分类结果
    intent_classification: Optional[dict]

    # 当前活跃的 Agent 类型
    active_agent: str

    # Agent 生成的回答
    agent_response: str

    # 质量评估
    quality_score: float
    quality_feedback: str

    # 重试计数
    retry_count: int

    # 升级信息
    escalation_info: Optional[dict]

    # 最终输出
    final_response: str


# ========== 图构建 ==========
def build_customer_service_graph(llm, agents: dict):
    """构建客服系统工作流图

    Args:
        llm: 语言模型实例
        agents: 专业 Agent 字典，格式为 {name: agent_runnable}
    """
    graph = StateGraph(CustomerServiceState)

    # ---- 添加节点 ----

    # 1. 意图分类节点
    async def classify_intent_node(state):
        from intent_classifier import classify_intent
        user_msg = state["messages"][-1].content
        result = await classify_intent(llm, user_msg)
        return {
            "intent_classification": result.model_dump(),
            "active_agent": result.intent.value,
        }

    graph.add_node("classify_intent", classify_intent_node)

    # 2. 专业 Agent 节点
    async def run_agent_node(state, agent_name: str):
        agent = agents[agent_name]
        response = await agent.ainvoke({
            "messages": state["messages"],
        })
        # 提取回答文本
        if isinstance(response, dict) and "messages" in response:
            answer = response["messages"][-1].content
        else:
            answer = str(response)

        return {"agent_response": answer}

    # 为每个专业 Agent 创建节点
    for name in ["tech_support_agent", "order_service_agent", "product_agent", "general_agent"]:
        graph.add_node(name, lambda state, n=name: run_agent_node(state, n))

    # 3. 质量检查节点
    async def quality_check_node(state):
        from quality_checker import check_quality
        user_msg = state["messages"][-1].content
        ai_response = state["agent_response"]
        assessment = await check_quality(llm, user_msg, ai_response)
        return {
            "quality_score": assessment.score,
            "quality_feedback": assessment.feedback,
        }

    graph.add_node("quality_check", quality_check_node)

    # 4. 重新生成节点
    async def regenerate_node(state):
        """根据质量反馈重新生成回答"""
        from langchain_core.messages import SystemMessage, HumanMessage
        feedback = state.get("quality_feedback", "")
        original_response = state.get("agent_response", "")

        regen_prompt = f"""请改进以下回答。改进建议：{feedback}

原回答：{original_response}

请生成一个更好的回答。"""

        response = await llm.ainvoke([
            SystemMessage(content="你是一个专业的客服人员，请根据改进建议优化回答。"),
            HumanMessage(content=regen_prompt),
        ])

        return {
            "agent_response": response.content,
            "retry_count": state.get("retry_count", 0) + 1,
        }

    graph.add_node("regenerate", regenerate_node)

    # 5. 人工升级节点
    async def human_escalation_node(state):
        from escalation import create_escalation, format_escalation_message
        classification = state.get("intent_classification")
        user_msg = state["messages"][-1].content

        result = create_escalation(
            user_message=user_msg,
            conversation_history=state["messages"],
            classification=type('obj', (object,), classification)() if classification else None,
        )
        message = format_escalation_message(result)

        return {
            "escalation_info": result.model_dump(),
            "final_response": message,
        }

    graph.add_node("human_escalation", human_escalation_node)

    # 6. 输出节点
    def output_node(state):
        response = state.get("agent_response", "抱歉，暂时无法处理您的请求。")
        return {"final_response": response}

    graph.add_node("output", output_node)

    # ---- 定义边 ----

    # 起始 -> 意图分类
    graph.add_edge(START, "classify_intent")

    # 意图分类 -> 条件路由
    from routing import route_by_intent, should_regenerate

    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "tech_support_agent": "tech_support_agent",
            "order_service_agent": "order_service_agent",
            "product_agent": "product_agent",
            "general_agent": "general_agent",
            "human_escalation": "human_escalation",
        },
    )

    # 所有 Agent -> 质量检查
    for agent_name in ["tech_support_agent", "order_service_agent", "product_agent", "general_agent"]:
        graph.add_edge(agent_name, "quality_check")

    # 质量检查 -> 条件路由
    graph.add_conditional_edges(
        "quality_check",
        should_regenerate,
        {
            "regenerate": "regenerate",
            "output": "output",
        },
    )

    # 重新生成 -> 质量检查（循环）
    graph.add_edge("regenerate", "quality_check")

    # 输出 -> 结束
    graph.add_edge("output", END)

    # 人工升级 -> 结束
    graph.add_edge("human_escalation", END)

    return graph.compile()
```

---

## 完整项目代码

### 项目文件结构

```
multi_agent_cs/
├── main.py              # 主入口和测试
├── config.py            # 配置
├── state.py             # 状态定义
├── intent_classifier.py # 意图分类器
├── agents/              # 专业 Agent
│   ├── __init__.py
│   ├── tech_support.py  # 技术支持
│   ├── order_service.py # 订单服务
│   └── product.py       # 产品咨询
├── tools/               # 工具定义
│   ├── __init__.py
│   ├── kb_search.py     # 知识库搜索
│   ├── order_tools.py   # 订单工具
│   └── product_tools.py # 产品工具
├── routing.py           # 路由逻辑
├── quality_checker.py   # 质量检查
├── escalation.py        # 人工升级
├── graph.py             # LangGraph 图定义
├── requirements.txt     # 依赖
└── tests/               # 测试
    └── test_scenarios.py
```

### main.py - 完整主入口

```python
"""多Agent客服系统 - 主入口"""

import asyncio
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from graph import build_customer_service_graph
from agents.tech_support import TECH_SUPPORT_PROMPT
from agents.order_service import ORDER_SERVICE_PROMPT
from agents.product import PRODUCT_INQUIRY_PROMPT
from tools.kb_search import search_knowledge_base, create_support_ticket
from tools.order_tools import query_order, process_refund
from tools.product_tools import get_product_info, compare_products


def create_agents(llm):
    """创建各专业 Agent"""
    from langchain.agents import create_agent

    agents = {}

    # 技术支持 Agent
    agents["tech_support_agent"] = create_agent(
        model=llm,
        tools=[search_knowledge_base, create_support_ticket],
        system_prompt=TECH_SUPPORT_PROMPT,
    )

    # 订单服务 Agent
    agents["order_service_agent"] = create_agent(
        model=llm,
        tools=[query_order, process_refund],
        system_prompt=ORDER_SERVICE_PROMPT,
    )

    # 产品咨询 Agent
    agents["product_agent"] = create_agent(
        model=llm,
        tools=[get_product_info, compare_products],
        system_prompt=PRODUCT_INQUIRY_PROMPT,
    )

    # 通用 Agent（无工具）
    agents["general_agent"] = create_agent(
        model=llm,
        tools=[],
        system_prompt="你是一个友好的客服助手，请礼貌地回答用户的一般性问题。",
    )

    return agents


async def run_conversation(graph, user_message: str):
    """运行单次对话"""
    print(f"\n{'='*60}")
    print(f"用户: {user_message}")
    print(f"{'='*60}")

    result = await graph.ainvoke({
        "messages": [HumanMessage(content=user_message)],
        "intent_classification": None,
        "active_agent": "",
        "agent_response": "",
        "quality_score": 0.0,
        "quality_feedback": "",
        "retry_count": 0,
        "escalation_info": None,
        "final_response": "",
    })

    # 输出结果
    intent = result.get("intent_classification", {})
    print(f"\n[意图分类] {intent.get('intent', '未知')}")
    print(f"[置信度]   {intent.get('confidence', 0):.2f}")
    print(f"[理由]     {intent.get('reasoning', '无')}")
    print(f"[质量分]   {result.get('quality_score', 0):.2f}")
    print(f"[重试次数] {result.get('retry_count', 0)}")
    print(f"\n客服回答: {result['final_response']}")

    if result.get("escalation_info"):
        print(f"\n[已升级] {result['escalation_info']}")

    return result


async def main():
    """主函数"""
    # 初始化 LLM
    llm = init_chat_model("groq:llama-3.3-70b-versatile")

    # 创建 Agent
    agents = create_agents(llm)

    # 构建工作流图
    graph = build_customer_service_graph(llm, agents)

    # 测试场景
    test_messages = [
        "我登录系统时一直报错，错误代码 403",
        "我的订单 ORD-20260501-001 到哪了？",
        "你们的高级课程包含哪些内容？",
        "我要投诉！你们的产品质量太差了，要求退款！",
        "你好",
    ]

    for msg in test_messages:
        await run_conversation(graph, msg)
        print("\n" + "-" * 60)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 测试场景

### 测试用例设计

```python
"""测试场景 - 覆盖各种客服场景"""

import pytest


# ========== 基础路由测试 ==========
class TestIntentRouting:
    """测试意图路由准确性"""

    def test_technical_support_routing(self):
        """技术支持类问题应路由到技术支持 Agent"""
        test_cases = [
            "我登录不上去了",
            "系统报错 500",
            "软件打不开怎么办",
            "页面加载很慢",
        ]
        # 验证每个测试用例都被分类为 technical_support
        for msg in test_cases:
            # 使用 classify_intent 验证
            pass

    def test_order_service_routing(self):
        """订单类问题应路由到订单服务 Agent"""
        test_cases = [
            "查一下我的订单 ORD-20260501-001",
            "快递到哪了？",
            "我要退货",
            "发票怎么开？",
        ]
        for msg in test_cases:
            pass

    def test_product_inquiry_routing(self):
        """产品咨询应路由到产品 Agent"""
        test_cases = [
            "高级课程多少钱？",
            "课程包含什么内容？",
            "基础版和高级版有什么区别？",
        ]
        for msg in test_cases:
            pass


# ========== 边界情况测试 ==========
class TestEdgeCases:
    """测试边界情况"""

    def test_ambiguous_message(self):
        """模糊消息应路由到通用 Agent"""
        test_cases = [
            "你好",
            "嗯",
            "在吗？",
        ]
        for msg in test_cases:
            pass

    def test_escalation_trigger(self):
        """敏感问题应触发人工升级"""
        test_cases = [
            "我要找你们律师谈",
            "我要去消费者协会投诉",
            "这个问题我报了警",
        ]
        for msg in test_cases:
            pass

    def test_multi_intent_message(self):
        """多意图消息应识别主要意图"""
        msg = "我的订单还没到，而且你们的系统一直报错"
        # 应识别为主要意图是订单问题或技术支持


# ========== 质量检查测试 ==========
class TestQualityCheck:
    """测试质量检查机制"""

    def test_low_quality_triggers_regeneration(self):
        """低质量回答应触发重新生成"""
        pass

    def test_max_retry_count(self):
        """重试次数不应超过上限"""
        pass


# ========== 完整流程测试 ==========
class TestEndToEnd:
    """端到端测试"""

    def test_full_technical_support_flow(self):
        """完整技术支持流程：分类 -> 处理 -> 质量检查 -> 输出"""
        pass

    def test_full_order_service_flow(self):
        """完整订单服务流程"""
        pass

    def test_escalation_flow(self):
        """人工升级完整流程"""
        pass
```

### 手动测试脚本

```python
"""手动交互测试"""

async def interactive_test():
    """交互式测试模式"""
    from langchain.chat_models import init_chat_model
    from graph import build_customer_service_graph
    from main import create_agents

    llm = init_chat_model("groq:llama-3.3-70b-versatile")
    agents = create_agents(llm)
    graph = build_customer_service_graph(llm, agents)

    print("多Agent客服系统 - 交互测试模式")
    print("输入 'quit' 退出\n")

    while True:
        user_input = input("用户: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        if not user_input:
            continue

        await run_conversation(graph, user_input)
```

---

## 常见错误

### 1. 结构化输出解析失败

```
错误: pydantic.ValidationError: 1 validation error for IntentClassification
```

**原因**：LLM 返回的格式不符合 Pydantic 模型定义。

**解决方案**：
```python
# 确保 Pydantic 模型的 Field 有清晰的 description
class IntentClassification(BaseModel):
    intent: IntentType = Field(
        description="用户的主要意图类别，必须是以下之一：technical_support, order_service, ..."
    )
```

### 2. 条件边返回值不匹配

```
错误: KeyError: 'xxx'  # 在 conditional_edges 的 mapping 中
```

**原因**：路由函数的返回值与 `add_conditional_edges` 的 mapping 字典的 key 不匹配。

**解决方案**：
```python
# 确保路由函数的返回值与 mapping 完全一致
def route_by_intent(state):
    return "tech_support_agent"  # 必须与 mapping 中的 key 完全匹配

graph.add_conditional_edges(
    "classify_intent",
    route_by_intent,
    {
        "tech_support_agent": "tech_support_agent",  # key 要与返回值一致
        # ...
    },
)
```

### 3. Agent 工具调用格式错误

```
错误: ToolException: Invalid tool input
```

**原因**：工具函数的参数类型注解或 docstring 不清晰。

**解决方案**：确保每个工具都有完整的 docstring 和类型注解：
```python
@tool
def my_tool(param1: str, param2: int = 10) -> str:
    """工具的详细描述，说明每个参数的含义。

    Args:
        param1: 第一个参数的说明
        param2: 第二个参数的说明，默认值为 10
    """
    return f"结果: {param1}, {param2}"
```

---

## 最佳实践

1. **意图类别设计**：类别不宜过多（建议 5-8 个），过多会降低分类准确率
2. **置信度阈值**：当分类置信度低于 0.5 时，考虑路由到通用 Agent 或要求用户澄清
3. **质量检查开销**：质量检查会增加延迟，生产环境中可根据需要跳过简单问题的检查
4. **错误处理**：每个节点都应有 try-except，避免单点故障导致整个流程中断
5. **对话历史管理**：传递给 Agent 的对话历史不宜过长，建议只保留最近 5-10 轮
6. **工具权限控制**：敏感操作（如退款）应有人工确认机制，不应完全自动化
7. **监控与日志**：记录每次分类结果、路由决策、质量评分，用于后续优化

---

## 练习题

### 基础练习

1. **新增意图类别**：添加一个"售后服务"类别，包含保修查询、维修预约等功能
2. **自定义质量标准**：修改质量检查提示词，增加对"回答长度"的评估
3. **添加对话记忆**：使系统支持多轮对话，记住之前的上下文

### 进阶练习

4. **并行检索**：当用户问题涉及多个领域时，同时调用多个 Agent 的工具
5. **动态工具加载**：根据用户类型（VIP/普通）加载不同的工具集
6. **回答模板化**：为不同类型的问题设计标准回答模板

### 挑战练习

7. **Agent 间协作**：实现 Agent 之间的信息传递，如技术支持确认订单信息
8. **学习机制**：记录低质量回答和用户反馈，持续优化提示词
9. **多语言支持**：扩展系统支持中英文双语客服

---

> **上一章**：[24 - 项目实战：RAG 系统](./24-项目实战-RAG系统.md)
> **下一章**：[26 - 项目实战：研究助手](./26-项目实战-研究助手.md)
