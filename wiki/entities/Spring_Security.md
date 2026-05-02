---
title: "Spring Security"
type: entity
tags: [Spring Security, 安全, 认证, 授权]
sources: [raw/01-articles/Spring-boot/spring-boot-security/]
last_updated: 2026-05-01
---

## 定义

Spring Security 是 Spring 生态中的安全框架，提供认证（Authentication）和授权（Authorization）功能，保护应用程序免受常见安全威胁。

## 关键信息

- **认证**：验证用户身份（用户名/密码、OAuth2、JWT 等）
- **授权**：控制用户访问权限（角色、权限、URL 级别）
- **CSRF 防护**：跨站请求伪造保护
- **会话管理**：会话固定攻击防护、并发会话控制
- **密码加密**：BCryptPasswordEncoder 等加密方式

## Spring Boot 整合

- **依赖**：`spring-boot-starter-security`
- **配置类**：`SecurityConfig` 继承 `WebSecurityConfigurerAdapter`
- **自定义登录**：配置登录页面、成功/失败处理器

## 关联连接

- [[摘要-spring-boot-知识库]] — 来源
- [[Spring_Boot]] — 框架整合
