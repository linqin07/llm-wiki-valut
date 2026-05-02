---
title: "Druid"
type: entity
tags: [Druid, 数据库, 连接池, 监控]
sources: [raw/01-articles/Spring-boot/spring-boot-druid/]
last_updated: 2026-05-01
---

## 定义

Druid 是阿里巴巴开源的数据库连接池实现，提供了强大的监控和扩展功能，是目前 Java 生态中最流行的数据库连接池之一。

## 关键信息

- **监控功能**：内置 StatViewServlet 提供 Web 监控界面
- **防火墙**：WallFilter 防御 SQL 注入攻击
- **慢 SQL 记录**：可配置慢 SQL 阈值并记录
- **连接池配置**：initialSize、minIdle、maxActive、maxWait 等参数
- **过滤器**：stat（统计）、wall（防火墙）、log4j（日志）

## Spring Boot 整合

- **依赖**：`druid-spring-boot-starter`
- **配置类**：`DruidConfiguration` 配置监控 Servlet 和 Filter
- **访问地址**：`http://localhost:8080/druid/index.html`
- **IP 白名单**：通过 `addInitParameter("allow", "...")` 配置

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[Spring_Boot]] — 框架整合
- [[MyBatis]] — ORM 整合
- [[JPA]] — 持久化整合
