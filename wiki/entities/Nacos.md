---
title: "Nacos"
type: entity
tags: [Spring-Cloud, Alibaba, 配置中心, 服务发现]
sources: [raw/01-articles/SpringCloud/4.接入nacos.md]
last_updated: 2026-05-01
---

## 定义

Nacos（Dynamic Naming and Configuration Service）是阿里巴巴开源的服务治理组件，同时提供服务注册发现和动态配置管理功能，是 Spring Cloud Alibaba 的核心组件。

## 关键信息

### 核心功能
- **服务发现**：支持 DNS 和 RPC 两种服务发现方式
- **配置管理**：集中管理配置，支持动态刷新（通过 `@RefreshScope`）
- **命名空间隔离**：通过 namespace 实现多环境隔离

### Spring Boot 接入

**依赖**：
- `spring-cloud-starter-alibaba-nacos-config` — 配置中心
- `spring-cloud-starter-alibaba-nacos-discovery` — 服务发现
- `spring-cloud-context` — 支持 `@RefreshScope` 动态刷新

**版本兼容性**：Spring Cloud 版本需与 Spring Boot 版本匹配（如 Hoxton.SR1）

### 多环境配置
```yaml
spring:
  profiles:
    active: ${profiles}
  application:
    name: appName
---
spring:
  profiles: local
  cloud:
    nacos:
      discovery:
        server-addr: 10.1.1.1:8848
        enabled: false
      config:
        server-addr: 10.1.1.1:8848
        file-extension: yml
        group: DEFAULT_GROUP
        enabled: false
```

- **local**：本地环境可关闭 discovery 和 config
- **dev**：通过 `namespace` UUID 隔离开发环境

## 关联连接
- [[摘要-spring-cloud-微服务]] — 来源
- [[服务注册中心]] — 核心概念
- [[Eureka]] — 同类组件
- [[Spring_Boot]] — 基础框架
