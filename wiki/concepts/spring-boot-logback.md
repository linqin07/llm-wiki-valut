---
title: "spring-boot-logback"
type: concept
tags: [Spring Boot, 日志, Logback]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Spring-boot]]"
last_updated: 2026-05-01
---

## 定义

Logback 是 Spring Boot 默认的日志框架，是 Log4j 的继任者，提供更好的性能和更丰富的功能。

## 核心组件

- **Logger**：日志记录器，定义日志级别
- **Appender**：日志输出目的地（控制台、文件、数据库等）
- **Layout/Encoder**：日志格式化器

## 日志级别

- TRACE < DEBUG < INFO < WARN < ERROR
- Spring Boot 默认级别：INFO

## 配置方式

- **application.yml**：简单配置日志级别和文件路径
- **logback-spring.xml**：高级配置，支持环境区分、日志滚动、异步输出等

## 关联连接

- [[Spring_Boot]] — 框架实体
- [[摘要-spring-boot-知识库]] — 来源
- [[raw/09-archive/设计模式/raw/09-archive/Spring-boot/spring-boot-logback]] — 原始素材
