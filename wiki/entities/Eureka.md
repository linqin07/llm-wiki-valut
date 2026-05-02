---
title: "Eureka"
type: entity
tags: [Spring-Cloud, Netflix, 服务注册, 服务发现]
sources: [raw/01-articles/SpringCloud/1.Eureka服务注册中心.md]
last_updated: 2026-05-01
---

## 定义

Eureka 是 Netflix 开源的服务注册与发现组件，是 Spring Cloud Netflix 的核心模块之一。它基于 AP 原则（可用性 + 分区容错性）构建，适合作为微服务架构中的服务注册中心。

## 关键信息

### 核心特性
- 基于 AP 原则构建，保证服务可用性
- 服务实例通过心跳机制维持注册状态
- 提供 Web 管理界面（默认端口 8761）

### 搭建步骤
1. **依赖**：引入 `spring-cloud-starter-netflix-eureka-server`
2. **启动类**：添加 `@EnableEurekaServer` 注解
3. **配置**：设置 `registerWithEureka: false` 和 `fetchRegistry: false`（注册中心不注册自身）

### 开发调试技巧
- 通过 `@RibbonClients(defaultConfiguration = CustomizeLoadBalance.class)` 自定义负载均衡
- 实现 `AbstractLoadBalancerRule` 可过滤特定 IP 段的服务实例（如排除本地 192.168.20.x）
- 使用 `@ConditionalOnProperty` 按环境切换负载均衡策略（dev/prod）

### bootstrap.yml 配置
```yaml
spring:
  application:
    name: eureka
  cloud:
    config:
      enabled: false
      uri: ${CONFIG_SERVER_URL:http://localhost:8888}
```

## 关联连接
- [[摘要-spring-cloud-微服务]] — 来源
- [[服务注册中心]] — 核心概念
- [[CAP定理]] — AP 原则的理论基础
- [[Nacos]] — 替代方案（同时支持 CP 和 AP）
- [[Spring_Cloud_Gateway]] — 通过 Eureka 实现服务发现路由
- [[Spring_Boot]] — 基础框架
