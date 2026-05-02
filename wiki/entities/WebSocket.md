---
title: "WebSocket"
type: entity
tags: [WebSocket, 实时通信, 全双工]
sources: [raw/01-articles/Spring-boot/spring-boot-websocket/]
last_updated: 2026-05-01
---

## 定义

WebSocket 是一种在单个 TCP 连接上进行全双工通信的协议，允许服务器主动向客户端推送数据，实现真正的实时双向通信。

## 关键信息

- **全双工**：客户端和服务器可同时发送数据
- **低延迟**：相比 HTTP 轮询，减少延迟和带宽消耗
- **协议升级**：通过 HTTP Upgrade 机制建立连接
- **心跳机制**：Ping/Pong 帧保持连接活跃

## Spring Boot 整合

- **依赖**：`spring-boot-starter-websocket`
- **配置**：实现 `WebSocketConfigurer` 注册 Handler
- **集群部署**：使用 Redis 或消息队列实现多节点消息同步

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[Spring_Boot]] — 框架整合
