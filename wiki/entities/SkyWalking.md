---
title: "SkyWalking"
type: entity
tags: [APM, 分布式追踪, Apache, 开源]
sources:
  - "[[摘要-skywalking-源码调试]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Java学习/SkyWalking/源码调试]]"
last_updated: 2026-05-02
---

## 定义
Apache SkyWalking 是开源的应用性能监控（APM）系统，提供分布式追踪、服务网格遥测分析等功能。

## 核心概念
- **Span**：方法调用/RPC/数据库访问的最小单元
  - LocalSpan：普通 Java 方法调用
  - EntrySpan：应用服务入口/RPC 消费者
  - ExitSpan：应用服务出口/RPC 生产者/调用 redis/mysql
- **Trace Segment**：一个线程下所有 Span 的集合
- **TraceId**：调用链唯一标识，同一链条多次请求 ID 相同

## 编译要求
Maven 3.6+，从官网下载源码编译。

## 日志集成
logback 集成使用 apm-toolkit-logback-1.x 组件，可将 traceId 写入日志。

## 关联连接
- [[摘要-skywalking-源码调试]] — 来源
- [[raw/09-archive/设计模式/raw/09-archive/Java学习/SkyWalking/源码调试]] — 原始素材
