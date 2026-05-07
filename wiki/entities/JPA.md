---
title: "JPA"
type: entity
tags: [JPA, ORM, 数据库, Java]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/Spring-boot/整合JPA]]"
last_updated: 2026-05-01
---

## 定义

JPA（Java Persistence API）是 Java 持久化规范，定义了对象关系映射（ORM）的标准 API。Hibernate 是其最流行的实现。

## 关键信息

- **实体映射**：使用 `@Entity`、`@Table`、`@Column` 等注解映射数据库表
- **Repository**：Spring Data JPA 提供 `JpaRepository` 接口简化数据访问
- **查询方法**：方法名约定查询、`@Query` 注解查询、Specification 动态查询
- **事务管理**：`@Transactional` 注解声明事务边界
- **DDL 自动生成**：`spring.jpa.hibernate.ddl-auto` 配置自动建表

## Spring Boot 整合

- **依赖**：`spring-boot-starter-data-jpa`
- **配置**：数据源、JPA 属性（show-sql、ddl-auto 等）
- **多数据源**：配置多个 `DataSource` 和 `EntityManagerFactory`

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[Spring_Boot]] — 框架整合
- [[Druid]] — 数据源整合
- [[MyBatis]] — 替代方案
- [[raw/09-archive/Spring-boot/整合JPA]] — 原始素材
