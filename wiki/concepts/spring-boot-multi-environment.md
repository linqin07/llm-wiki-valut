---
title: "spring-boot-multi-environment"
type: concept
tags: [Spring Boot, 配置, 多环境]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Spring-boot]]"
last_updated: 2026-05-01
---

## 定义

多环境配置是 Spring Boot 中根据不同的运行环境（开发、测试、生产）加载不同配置文件的机制。

## 配置方式

### 1. Profile 配置文件
- `application.yml`：主配置文件
- `application-dev.yml`：开发环境
- `application-test.yml`：测试环境
- `application-prod.yml`：生产环境

### 2. 激活方式
- **配置文件**：`spring.profiles.active=dev`
- **命令行**：`--spring.profiles.active=dev`
- **JVM 参数**：`-Dspring.profiles.active=dev`
- **环境变量**：`SPRING_PROFILES_ACTIVE=dev`

### 3. 配置优先级
命令行参数 > JVM 参数 > 环境变量 > 配置文件

## 关联连接

- [[Spring_Boot]] — 框架实体
- [[spring-boot-deployment]] — 部署配置
- [[摘要-spring-boot-知识库]] — 来源
- [[raw/09-archive/设计模式/raw/09-archive/Spring-boot/通用]] — 原始素材
