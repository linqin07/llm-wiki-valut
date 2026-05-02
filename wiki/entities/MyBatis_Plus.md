---
title: "MyBatis-Plus"
type: entity
tags: [MyBatis-Plus, ORM, 代码生成, 增强]
sources: [raw/01-articles/Spring-boot/spring-boot-代码生成/MyBatis-Plus.md]
last_updated: 2026-05-01
---

## 定义

MyBatis-Plus 是 MyBatis 的增强工具，在 MyBatis 的基础上只做增强不做改变，为简化开发、提高效率而生。

## 关键信息

- **通用 CRUD**：内置通用 Mapper 和 Service，无需编写基础 SQL
- **条件构造器**：`QueryWrapper`、`LambdaQueryWrapper` 构建动态查询条件
- **分页插件**：内置分页插件，支持多种数据库
- **代码生成器**：快速生成 Entity、Mapper、Service、Controller 代码
- **逻辑删除**：支持逻辑删除，无需手动处理
- **自动填充**：创建时间、更新时间等字段自动填充

## Spring Boot 整合

- **依赖**：`mybatis-plus-boot-starter`
- **配置**：`mybatis-plus.mapper-locations`
- **BaseMapper**：继承 `BaseMapper<T>` 获得基础 CRUD 方法

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[MyBatis]] — 基础框架
- [[Spring_Boot]] — 框架整合
