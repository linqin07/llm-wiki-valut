---
title: "Akka"
type: entity
tags: [事件驱动, Actor模型, 异步编程, Scala]
sources: [raw/01-articles/Java学习/Netty/事件驱动框架.md]
last_updated: 2026-05-02
---

## 定义
Akka 是轻量级的异步、非阻塞、高性能事件驱动编程模型，通过 Actor 模型处理消息。

## 核心角色
- **ActorSystem**：创建 Actor 系统
- **ActorRef**：Actor 引用持有者，用于发送消息
- **AbstractActor**：Actor 具体实现

## AKKA-FSM（有限状态机）
- **优势**：高性能、异常处理、超时处理、状态机监控、事件追踪、定时器
- **劣势**：底层 Scala 实现源码难读、中文文档少

## 适用场景
复杂消息处理：多种消息类型、顺序依赖、循环处理

## 关联连接
- 事件驱动 — 设计模式
- [[Netty]] — 同类网络框架
- 摘要-事件驱动框架 — 来源
