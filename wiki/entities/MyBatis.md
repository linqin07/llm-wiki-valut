---
title: "MyBatis"
type: entity
tags: [MyBatis, ORM, 数据库, Java]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/Spring-boot/spring-boot-mybatis]]"
last_updated: 2026-05-01
---

## 定义

MyBatis 是一款优秀的持久层框架，支持定制化 SQL、存储过程以及高级映射。它避免了几乎所有的 JDBC 代码和手动设置参数以及获取结果集。

## 关键信息

- **SQL 映射**：通过 XML 或注解将 Java 方法映射到 SQL 语句
- **TypeHandler**：自定义类型处理器，处理 Java 类型与 JDBC 类型的转换
- **动态 SQL**：支持 `<if>`、`<choose>`、`<foreach>` 等动态 SQL 标签
- **分页**：可整合 PageHelper 插件实现物理分页
- **代码生成**：MyBatis Generator 自动生成实体、Mapper、XML 文件

## Spring Boot 整合

- **依赖**：`mybatis-spring-boot-starter`
- **配置**：`mybatis.mapper-locations` 指定 XML 文件位置
- **Mapper 扫描**：使用 `@MapperScan` 注解扫描 Mapper 接口
- **事务管理**：整合 Spring 事务管理，使用 `@Transactional` 注解

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[Spring_Boot]] — 框架整合
- [[Druid]] — 数据源整合
- [[SPI机制]] — JDBC 驱动加载机制
- [[MapStruct]] — 对象映射
- [[MyBatis_Plus]] — 增强工具
- [[raw/09-archive/Spring-boot/spring-boot-mybatis]] — 原始素材
