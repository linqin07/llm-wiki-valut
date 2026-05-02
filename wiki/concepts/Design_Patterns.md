---
title: "设计模式（Design Patterns）"
type: concept
tags: [设计模式, GoF, Java, 软件工程, 面向对象]
sources:
  - raw/01-articles/设计模式/
last_updated: 2026-05-01
---

## 定义

设计模式（Design Patterns）是软件开发中经过验证的、可重用的解决方案，用于解决在特定上下文中反复出现的设计问题。它们不是可以直接使用的代码，而是描述了在特定情况下如何解决一般设计问题的模板。

> 设计模式是前人经验的结晶，是面向对象设计中常见问题的最佳实践。

## GoF 设计模式分类

GoF（Gang of Four）将 23 种设计模式分为三大类：

### 创建型模式（Creational Patterns）

创建型模式关注对象的创建机制，试图以适合情况的方式创建对象。

| 模式 | 意图 | 核心问题 |
|------|------|----------|
| [[Singleton_Pattern]] | 保证一个类仅有一个实例，并提供全局访问点 | 全局使用的类频繁创建与销毁 |
| [[Factory_Pattern]] | 定义创建对象的接口，让子类决定实例化哪个类 | 对象创建逻辑复杂或多变 |
| [[Abstract_Factory_Pattern]] | 提供创建一系列相关依赖对象的接口 | 需要创建一组相关的对象 |
| [[Builder_Pattern]] | 将复杂对象的构建与表示分离 | 对象创建过程复杂，需要多种表示 |
| [[Prototype_Pattern]] | 通过复制原型创建新对象 | 创建对象成本高，需要相似对象 |

### 结构型模式（Structural Patterns）

结构型模式关注类和对象的组合，形成更大的结构。

| 模式 | 意图 | 核心问题 |
|------|------|----------|
| [[Adapter_Pattern]] | 将一个类的接口转换成客户希望的另一个接口 | 接口不兼容的类需要协同工作 |
| [[Decorator_Pattern]] | 动态地给对象添加额外职责 | 需要扩展对象功能，但不改变其接口 |
| [[Facade_Pattern]] | 为子系统提供统一的高层接口 | 子系统复杂，需要简化接口 |
| [[Bridge_Pattern]] | 将抽象部分与实现部分分离 | 抽象和实现需要独立变化 |
| [[Proxy_Pattern]] | 为其他对象提供代理以控制访问 | 需要控制对对象的访问 |
| [[Composite_Pattern]] | 将对象组合成树形结构 | 表示对象的部分-整体层次结构 |
| [[Flyweight_Pattern]] | 运用共享技术有效支持大量细粒度对象 | 大量相似对象消耗内存 |

### 行为型模式（Behavioral Patterns）

行为型模式关注对象之间的通信和职责分配。

| 模式 | 意图 | 核心问题 |
|------|------|----------|
| Chain_of_Responsibility_Pattern | 将请求的发送者和接收者解耦 | 多个对象可以处理请求，处理者不确定 |
| [[Command_Pattern]] | 将请求封装为对象 | 需要将请求排队、记录日志或支持撤销 |
| [[Interpreter_Pattern]] | 定义语言的文法表示 | 需要解释执行特定语言 |
| [[Iterator_Pattern]] | 提供顺序访问聚合对象元素的方法 | 需要遍历集合而不暴露其内部结构 |
| [[Mediator_Pattern]] | 用中介对象封装一系列对象交互 | 对象之间存在复杂的直接依赖关系 |
| [[Memento_Pattern]] | 在不破坏封装的前提下捕获对象状态 | 需要保存和恢复对象的历史状态 |
| [[Observer_Pattern]] | 定义一对多的依赖关系 | 一个对象状态改变需要通知多个对象 |
| [[State_Pattern]] | 允许对象在内部状态改变时改变行为 | 对象行为取决于其状态 |
| [[Strategy_Pattern]] | 定义算法族，封装每个算法 | 需要在运行时选择算法 |
| [[Template_Method_Pattern]] | 定义算法骨架，延迟某些步骤 | 算法结构固定，某些步骤可变 |
| [[Visitor_Pattern]] | 表示作用于对象结构的操作 | 需要对对象结构执行多种不相关操作 |

## 设计原则

设计模式遵循以下核心设计原则：

1. **单一职责原则（SRP）**：一个类只有一个引起变化的原因
2. **开闭原则（OCP）**：对扩展开放，对修改关闭
3. **里氏替换原则（LSP）**：子类可以替换父类
4. **接口隔离原则（ISP）**：客户端不应依赖不需要的接口
5. **依赖倒置原则（DIP）**：依赖抽象而非具体实现
6. **迪米特法则（LoD）**：最少知识原则
7. **组合优于继承**：优先使用对象组合而非类继承

## 模式选择指南

| 场景 | 推荐模式 |
|------|----------|
| 需要全局唯一实例 | [[Singleton_Pattern]] |
| 创建对象逻辑复杂 | [[Factory_Pattern]] 或 [[Builder_Pattern]] |
| 需要扩展对象功能 | [[Decorator_Pattern]] |
| 简化复杂子系统 | [[Facade_Pattern]] |
| 对象间需要解耦通信 | [[Observer_Pattern]] 或 [[Mediator_Pattern]] |
| 需要支持撤销操作 | [[Command_Pattern]] |
| 算法需要动态切换 | [[Strategy_Pattern]] |
| 对象行为随状态改变 | [[State_Pattern]] |

## 关联连接

- [[摘要-design-patterns-java]] — 来源摘要
- [[Singleton_Pattern]] — 单例模式详解
- [[Factory_Pattern]] — 工厂模式详解
- [[Observer_Pattern]] — 观察者模式详解
- [[Strategy_Pattern]] — 策略模式详解
