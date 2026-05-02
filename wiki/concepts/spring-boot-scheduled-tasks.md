---
title: "spring-boot-scheduled-tasks"
type: concept
tags: [Spring Boot, 定时任务, 调度]
sources: [raw/01-articles/Spring-boot/定时任务/]
last_updated: 2026-05-01
---

## 定义

定时任务是 Spring Boot 中按预定时间或周期执行任务的机制，支持多种实现方式。

## 实现方式

### 1. @Scheduled 注解
- `fixedRate`：固定频率执行（毫秒）
- `fixedDelay`：固定延迟执行（毫秒）
- `cron`：Cron 表达式定义执行时间
- 需要 `@EnableScheduling` 启用

### 2. 异步定时任务
- 使用 `@Async` 注解实现多线程并行执行
- 需要 `@EnableAsync` 启用
- 配置 `ThreadPoolTaskExecutor` 线程池

### 3. SchedulingConfigurer 动态配置
- 实现 `SchedulingConfigurer` 接口
- 从数据库读取 Cron 表达式，支持动态修改
- 修改后下下个周期生效

### 4. Quartz 框架
- 企业级任务调度框架
- 支持集群部署、任务持久化、故障恢复

## 关联连接

- [[Spring_Boot]] — 框架实体
- [[摘要-spring-boot-知识库]] — 来源
