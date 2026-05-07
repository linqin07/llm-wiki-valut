---
title: "Spring_Cloud_Gateway"
type: entity
tags: [Spring-Cloud, 网关, 路由, 过滤器]
sources:
  - "[[摘要-spring-cloud-微服务]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/SpringCloud/3.服务网关SpringCloudGateWay]]"
last_updated: 2026-05-01
---

## 定义

Spring Cloud Gateway 是 Spring Cloud 生态中的新一代 API 网关，基于 Spring WebFlux 和 Project Reactor 构建，用于替代 Netflix Zuul。提供统一的路由方式和基于 Filter 链的网关功能（安全、监控、限流）。

## 关键信息

### 核心概念
- **Route（路由）**：网关的基本构建块，由 ID、目标 URI、断言集合和过滤器集合组成
- **Predicate（断言）**：Java 8 Function Predicate，匹配 HTTP 请求的任意内容（头、参数等）
- **Filter（过滤器）**：在发送下游请求前后修改请求和响应

### 技术约束
- 基于 Netty + WebFlux，**不能在传统 Servlet 容器中运行**
- 不能引用 `spring-boot-starter-web`，否则会冲突
- 必须使用 Spring Boot 2.x

### 路由配置
```yaml
spring:
  cloud:
    gateway:
      routes:
      - id: path_route2
        uri: http://127.0.0.1:9090
        order: -1
        predicates:
        - Path=/**
      discovery:
        locator:
          enabled: true
          lower-case-service-id: true
```

- `order` 参数控制路由优先级（数值越小优先级越高）
- 整合 Eureka 后可通过 `lb://service-name` 实现负载均衡路由

### 过滤器体系

**Global filter**：应用于所有路由
- 实现 `GlobalFilter` 和 `Ordered` 接口
- 多个 filter 按 order 顺序执行（越小越优先），post 阶段逆序
- **注意**：globalFilter 和 gatewayFilter 在不同线程执行，ThreadLocal 不能共享

**GatewayFilter**：应用于单个路由或路由组
- 通过 `RouteLocator` 编程式绑定到特定路由

### 请求体读取方案

**方案一**：重写 `ModifyRequestBodyGatewayFilterFactory`
- 适用于 yml 配置路由，兼容性最好
- 通过 `ServerRequest.bodyToMono()` 读取请求体
- 支持 `application/x-www-form-urlencoded` 和 `application/json`

**方案二**：使用 `ReadBodyPredicateFactory`
- 适用于代码配置路由
- 通过 `.readBody()` 方法在路由断言中读取

### 响应报文修改
通过 `ServerHttpResponseDecorator` 包装响应，统一返回格式。Order 需设为 `-2`（在 response write filter `-1` 之前执行）。

## 关联连接
- [[摘要-spring-cloud-微服务]] — 来源
- [[服务网关]] — 核心概念
- [[Zuul]] — 前任网关方案
- [[Eureka]] — 服务发现集成
- [[SkyWalking]] — 分布式追踪 APM
- [[Spring_Boot]] — 基础框架
- [[raw/09-archive/设计模式/raw/09-archive/SpringCloud/3.服务网关SpringCloudGateWay]] — 原始素材
