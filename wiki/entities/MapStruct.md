---
title: "MapStruct"
type: entity
tags: [MapStruct, 对象映射, 代码生成]
sources: [raw/01-articles/Spring-boot/spring-boot-mybatis/7.MapStruct映射框架.md]
last_updated: 2026-05-01
---

## 定义

MapStruct 是一个 Java 注解处理器，用于生成类型安全的 Bean 映射代码。它在编译时生成映射代码，避免运行时反射开销。

## 关键信息

- **编译时生成**：通过注解处理器在编译期生成映射代码
- **类型安全**：编译时检查类型匹配，减少运行时错误
- **高性能**：无反射，直接调用 getter/setter
- **灵活配置**：支持自定义映射方法、多源参数、嵌套映射

## 核心注解

- `@Mapper`：标记接口为映射器
- `@Mapping`：配置字段映射规则
- `@Mappings`：多个映射配置
- `@InheritConfiguration`：继承其他映射配置

## Spring Boot 整合

- **依赖**：`mapstruct`、`mapstruct-processor`
- **组件模型**：`componentModel = "spring"` 自动生成 Spring Bean

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[MyBatis]] — ORM 整合
- [[Spring_Boot]] — 框架整合
- [[摘要-java-工具类]] — Java 工具类汇总
