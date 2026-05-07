---
title: 责任链模式（Chain of Responsibility Pattern）
type: concept
tags:
  - 设计模式
  - 行为型模式
  - Java
  - 解耦
  - 链式处理
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/责任链模式]]"
last_updated: 2026-05-07
---

## 定义

责任链模式（Chain of Responsibility Pattern）是一种行为型设计模式，将请求的发送者和接收者解耦，使多个对象都有机会处理这个请求。将这些对象连成一条链，并沿着这条链传递请求，直到有一个对象处理它为止。

**意图**：使多个对象都有机会处理请求，从而避免请求的发送者和接收者之间的耦合。

**主要解决**：多个对象可以处理请求，但处理者在运行时动态确定。

**何时使用**：
- 请假审批流程（组长 → 经理 → CEO）
- 报销审批流程（员工额度 → 经理额度 → CEO 额度）
- 日志处理（DEBUG → INFO → ERROR）
- Web 过滤器链

## 核心角色

- **Handler（抽象处理者）**：定义处理请求的接口，持有下一个处理者的引用
- **ConcreteHandler（具体处理者）**：实现处理请求的逻辑，处理不了则传递给下一个

## 代码示例

**抽象审批人：**

```java
public abstract class Approver {
    protected String name;
    protected Approver nextApprover;

    public Approver(String name) {
        this.name = name;
    }

    public Approver setNextApprover(Approver nextApprover) {
        this.nextApprover = nextApprover;
        return this.nextApprover;
    }

    public abstract void approve(int amount);
}
```

**具体审批人：**

```java
public class Staff extends Approver {
    public Staff(String name) { super(name); }

    @Override
    public void approve(int amount) {
        if (amount <= 1000) {
            System.out.println("审批通过。【员工：" + name + "】");
        } else {
            System.out.println("无权审批，升级处理。【员工：" + name + "】");
            this.nextApprover.approve(amount);
        }
    }
}
```

**使用：**

```java
Approver approver = new Staff("张三");
approver.setNextApprover(new Manager("李四"))
        .setNextApprover(new CEO("王五"));
approver.approve(8000);
// 无权审批，升级处理。【员工：张三】
// 无权审批，升级处理。【经理：李四】
// 审批通过。【CEO：王五】
```

## 注意事项

1. **启动顺序**：必须从链头（第一个处理者）启动
2. **变量共享问题**：抽象类私有变量通过 `new` 注入不会共享，解决方案：使用 `static` 变量或通过构造方法参数传递
3. **异常处理**：每一层的异常是本层处理还是向上抛出，需根据业务决定

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Command_Pattern]] — 命令模式
- [[State_Pattern]] — 状态模式
- [[Observer_Pattern]] — 观察者模式
- [[raw/09-archive/设计模式/责任链模式]] — 原始素材
