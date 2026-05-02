---
title: "spring-boot-auto-configuration"
type: concept
tags: [Spring Boot, 自动装配, 配置]
sources: [raw/01-articles/Spring-boot/spring-boot-源码解析/自动装配.md]
last_updated: 2026-05-01
---

## 定义

自动装配（Auto-Configuration）是 Spring Boot 的核心特性之一，它根据类路径中的依赖和配置文件自动配置 Spring 应用程序的 Bean。

## 核心机制

- **@EnableAutoConfiguration**：启用自动配置的注解
- **@Import(AutoConfigurationImportSelector.class)**：导入自动配置选择器
- **spring.factories**：在 `META-INF/spring.factories` 中定义自动配置类
- **条件注解**：`@ConditionalOnClass`、`@ConditionalOnBean`、`@ConditionalOnProperty` 等控制配置生效条件

## 执行流程

1. `@SpringBootApplication` 触发 `@EnableAutoConfiguration`
2. `AutoConfigurationImportSelector` 加载 `spring.factories` 中的配置类
3. 根据条件注解过滤出需要生效的配置类
4. 配置类中的 `@Bean` 方法注册到容器

## 关联连接

- [[Spring_Boot]] — 框架实体
- [[摘要-spring-boot-知识库]] — 来源
