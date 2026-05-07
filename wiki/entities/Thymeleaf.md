---
title: "Thymeleaf"
type: entity
tags: [Thymeleaf, 模板引擎, 前端]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Spring-boot]]"
last_updated: 2026-05-01
---

## 定义

Thymeleaf 是一个现代化的服务器端 Java 模板引擎，适用于 Web 和独立环境。它能够处理 HTML、XML、JavaScript、CSS 甚至纯文本。

## 关键信息

- **自然模板**：模板文件可直接在浏览器中预览
- **表达式语言**：使用 `th:text`、`th:if`、`th:each` 等属性
- **布局**：支持 Fragment 和 Layout 方式复用页面组件
- **Spring 集成**：原生支持 Spring 表达式语言（SpEL）

## Spring Boot 整合

- **依赖**：`spring-boot-starter-thymeleaf`
- **配置**：`spring.thymeleaf.prefix`、`spring.thymeleaf.suffix`
- **模板位置**：默认 `resources/templates/`

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[Spring_Boot]] — 框架整合
- [[JSP]] — 替代方案
- [[raw/09-archive/设计模式/raw/09-archive/Spring-boot/spring-boot-typmeleaf]] — 原始素材
