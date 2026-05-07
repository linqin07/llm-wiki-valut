---
title: "spring-boot-aop"
type: concept
tags: [Spring Boot, AOP, 日志, 切面]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Spring-boot]]"
last_updated: 2026-05-01
---

## 定义

AOP（面向切面编程）是 Spring 框架的核心特性之一，用于将横切关注点（如日志、事务、安全）从业务逻辑中分离出来。

## 核心概念

- **切面（Aspect）**：横切关注点的模块化
- **连接点（JoinPoint）**：程序执行的特定点
- **通知（Advice）**：在连接点执行的动作（Before、After、Around、AfterReturning、AfterThrowing）
- **切入点（Pointcut）**：匹配连接点的表达式

## Spring Boot 整合

- **依赖**：`spring-boot-starter-aop`
- **注解**：`@Aspect`、`@Component`、`@Pointcut`、`@Before`、`@After`、`@Around`
- **应用场景**：统一日志记录、性能监控、权限校验、事务管理

## 关联连接

- [[Spring_Boot]] — 框架实体
- [[摘要-spring-boot-知识库]] — 来源
- [[raw/09-archive/设计模式/raw/09-archive/Spring-boot]] — 原始素材
