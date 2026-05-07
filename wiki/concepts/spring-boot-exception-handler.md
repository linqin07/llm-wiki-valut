---
title: "spring-boot-exception-handler"
type: concept
tags: [Spring Boot, 异常处理, 错误处理]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Spring-boot]]"
last_updated: 2026-05-01
---

## 定义

全局异常处理是 Spring Boot 中统一处理应用程序异常的机制，通过 `@ControllerAdvice` 和 `@ExceptionHandler` 注解实现。

## 核心注解

- **@ControllerAdvice**：定义全局异常处理类
- **@ExceptionHandler**：标记处理特定异常的方法
- **@RestControllerAdvice**：组合 `@ControllerAdvice` 和 `@ResponseBody`

## 最佳实践

- 自定义业务异常类，包含错误码和错误信息
- 统一异常响应格式，返回 JSON 格式的错误信息
- 区分已知业务异常和未知系统异常，分别处理
- 记录异常日志，便于排查问题

## 关联连接

- [[Spring_Boot]] — 框架实体
- [[摘要-spring-boot-知识库]] — 来源
- [[raw/09-archive/设计模式/raw/09-archive/Spring-boot]] — 原始素材
