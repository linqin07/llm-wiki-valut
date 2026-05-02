---
title: "Netty"
type: entity
tags: [网络框架, Java, 异步, 事件驱动]
sources: [raw/01-articles/Java学习/Netty/Netty实战.md]
last_updated: 2026-05-02
---

## 定义
Netty 是基于 Java NIO 的异步事件驱动网络应用框架，简化了 TCP/UDP 服务器开发。

## 核心组件
- **Channel**：数据传输载体
- **EventLoop**：事件循环，一个 EventLoop 绑定一个 Thread，可服务多个 Channel
- **ChannelFuture**：异步操作结果通知
- **ChannelHandler / ChannelPipeline**：处理入站出站数据的责任链

## ByteBuf
维护读写两个索引，支持三种模式：
- 堆缓冲区（Heap Buffer）
- 直接缓冲区（Direct Buffer）
- 复合缓冲区（Composite Buffer）

## 传输模式
- OIO：阻塞模式
- NIO：异步非阻塞（推荐）
- Local：JVM 内部通信
- Embedded：测试用

## 零拷贝
仅在 NIO 和 Epoll 传输时可用，可显著提升 FTP/HTTP 等协议性能。

## 关联连接
- [[事件驱动]] — 设计模式
- [[异步非阻塞IO]] — IO 模型
- [[摘要-netty-实战]] — 来源
