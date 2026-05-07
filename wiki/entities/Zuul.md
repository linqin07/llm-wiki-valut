---
title: "Zuul"
type: entity
tags: [Spring-Cloud, Netflix, 网关, 路由]
sources:
  - "[[摘要-spring-cloud-微服务]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/SpringCloud/5.zuul 网关]]"
last_updated: 2026-05-01
---

## 定义

Zuul 是 Netflix 开源的 API 网关服务，是 Spring Cloud Netflix 的组件之一。提供动态路由、监控、弹性负载和安全等功能。在 Spring Cloud 生态中逐渐被 [[Spring_Cloud_Gateway]] 替代。

## 关键信息

### 文件上传问题
大文件经过 Zuul 转发会消耗 JVM 内存，并导致连接超时。

**解决方案**：在请求路径加 `/zuul` 前缀跳过转发
- 原路径：`/vpa/skill/A` → 改为：`/vpa/zuul/skill/A`
- 文件资源不会消耗 JVM 内存

### 超时配置
```properties
zuul.host.connect-timeout-millis=300000
zuul.host.socket-timeout-millis=300000
ribbon.ReadTimeout=300000
ribbon.ConnectTimeout=300000
hystrix.command.default.execution.isolation.thread.timeoutInMilliseconds=60000
```

### 路由配置
```yaml
zuul.routes.vpa-skill.path=/skill/**
zuul.routes.vpa-skill.serviceId=vpa-service-skill
```

## 关联连接
- [[摘要-spring-cloud-微服务]] — 来源
- [[服务网关]] — 核心概念
- [[Spring_Cloud_Gateway]] — 替代方案
- [[Spring_Boot]] — 基础框架
- [[raw/09-archive/设计模式/raw/09-archive/SpringCloud/5.zuul 网关]] — 原始素材
