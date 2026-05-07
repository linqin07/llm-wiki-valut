---
title: "spring-boot-json"
type: concept
tags: [Spring Boot, JSON, 序列化, Jackson]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Spring-boot]]"
last_updated: 2026-05-01
---

## 定义

JSON 处理是 Spring Boot 中数据序列化和反序列化的核心机制，默认使用 Jackson 库处理 JSON 格式数据。

## 核心特性

- **Jackson**：Spring Boot 默认 JSON 处理库
- **@JsonProperty**：自定义序列化字段名
- **@JsonFormat**：格式化日期、数字等类型
- **@JsonIgnore**：忽略特定字段
- **@JsonSerialize/@JsonDeserialize**：自定义序列化/反序列化器

## 常见场景

- **LocalDateTime 格式化**：配置全局日期格式
- **枚举序列化**：枚举与 JSON 值的互转
- **参数校验**：结合 `@Valid` 注解校验请求参数
- **空值处理**：配置 null 值的序列化策略

## 关联连接

- [[Spring_Boot]] — 框架实体
- [[摘要-spring-boot-知识库]] — 来源
- [[raw/09-archive/设计模式/raw/09-archive/Spring-boot/spring-boot-json]] — 原始素材
