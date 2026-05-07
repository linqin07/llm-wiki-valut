---
title: "GraphQL"
type: entity
tags: [GraphQL, API, 查询语言]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Spring-boot]]"
last_updated: 2026-05-01
---

## 定义

GraphQL 是一种用于 API 的查询语言，是由 Facebook 开发的数据查询和操作语言。它允许客户端精确指定需要的数据结构，避免过度获取或不足获取数据的问题。

## 关键信息

- **Schema 定义**：使用类型系统定义 API 的结构，包括 `type`、`input`、`enum` 等
- **Query 与 Mutation**：Query 用于查询（并行执行），Mutation 用于变更（串行执行）
- **标量类型**：Int、Float、String、Boolean、ID
- **非空标记**：使用 `!` 表示非空字段，如 `String!`
- **内省**：通过 `__schema` 和 `__type` 查询 API 支持的接口和类型

## Spring Boot 整合

- **依赖**：`graphql-spring-boot-starter`、`graphiql-spring-boot-starter`
- **自定义标量**：使用 `graphql-java-extended-scalars` 库扩展 Long、Date 等类型
- **Schema 文件**：放置在 `resources/graphql` 目录下，使用 `.graphqls` 扩展名
- **Resolver**：实现 `GraphQLQueryResolver` 接口处理查询逻辑

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[Spring_Boot]] — 框架整合
- [[Swagger]] — API 文档对比
- [[raw/09-archive/设计模式/raw/09-archive/Spring-boot/Graphql]] — 原始素材
