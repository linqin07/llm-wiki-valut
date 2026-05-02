---
title: Spring Boot
type: entity
tags:
  - SpringBoot
  - Java
  - 后端框架
  - 微服务
sources:
  - raw/01-articles/Spring-boot/
last_updated: 2026-05-01
---

## 定义

Spring Boot 是基于 Spring 框架的快速开发脚手架，通过约定优于配置的理念，简化 Spring 应用的创建、配置和部署过程。它内嵌 Tomcat/Jetty/Undertow 服务器，提供自动配置、起步依赖、Actuator 监控等特性。

## 关键信息

- **起步依赖（Starters）**：通过 `spring-boot-starter-*` 快速引入所需功能模块
- **自动配置（Auto-Configuration）**：根据类路径和配置自动配置 Bean
- **内嵌服务器**：无需外部 WAR 部署，直接运行 JAR 包
- **Actuator**：提供生产级监控和管理端点
- **多环境配置**：通过 `spring.profiles.active` 切换不同环境配置
- **配置文件**：支持 `application.properties` 和 `application.yml` 格式

## 核心注解

- `@SpringBootApplication`：组合注解，包含 `@Configuration`、`@EnableAutoConfiguration`、`@ComponentScan`
- `@ConditionalOnExpression`：根据表达式条件决定是否注入 Bean
- `@ConditionalOnBean`：当容器中存在指定 Bean 时才生效
- `@Primary`：自动装配时多个候选 Bean 的首选
- `@PostConstruct`：Bean 实例化后立即执行的方法

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[摘要-spring-mvc-实践]] — Spring MVC 实践
- [[摘要-spring-技术点]] — Bean/事务/嵌套分析
- [[spring-boot-json]] — JSON 序列化
- [[spring-boot-logback]] — 日志配置
- [[spring-boot-auto-configuration]] — 自动装配机制
- [[spring-boot-deployment]] — 部署方式
- [[spring-boot-multi-environment]] — 多环境配置
- [[MyBatis]] — ORM 整合
- [[JPA]] — 持久化整合
- [[Spring_Security]] — 安全整合
- [[Redis]] — 缓存整合
