---
title: "Swagger"
type: entity
tags: [Swagger, API, 文档, 测试]
sources: [raw/01-articles/Spring-boot/spring-boot-swagger/]
last_updated: 2026-05-01
---

## 定义

Swagger 是一套 API 文档自动生成和测试工具，通过注解标记 Controller 和方法，自动生成可交互的 API 文档界面。

## 关键信息

- **注解驱动**：使用 `@Api`、`@ApiOperation`、`@ApiParam` 等注解描述 API
- **UI 界面**：Swagger UI 提供在线 API 测试界面
- **代码生成**：可根据 OpenAPI 规范生成客户端代码
- **版本管理**：支持多版本 API 文档

## Spring Boot 整合

- **依赖**：`springfox-boot-starter` 或 `swagger-spring-boot-starter`
- **配置类**：`SwaggerConfig` 配置 Docket Bean
- **访问地址**：`http://localhost:8080/swagger-ui/`

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[Spring_Boot]] — 框架整合
- [[GraphQL]] — 替代方案
