---
title: "spring-boot-interceptor"
type: concept
tags: [Spring Boot, 拦截器, 过滤器]
sources:
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Spring-boot]]"
last_updated: 2026-05-01
---

## 定义

拦截器（Interceptor）是 Spring MVC 提供的请求处理机制，在请求到达 Controller 之前和之后执行特定逻辑。

## 核心接口

- **HandlerInterceptor**：定义三个方法
  - `preHandle`：请求处理之前执行
  - `postHandle`：请求处理之后、视图渲染之前执行
  - `afterCompletion`：请求完成之后执行

## 与过滤器的区别

- **过滤器（Filter）**：Servlet 规范，作用于所有请求
- **拦截器（Interceptor）**：Spring MVC 框架，仅作用于 Controller 请求
- 执行顺序：Filter → Interceptor → Controller → Interceptor → Filter

## Spring Boot 整合

- **注册**：实现 `WebMvcConfigurer` 的 `addInterceptors` 方法
- **配置**：指定拦截路径、排除路径、执行顺序

## 关联连接

- [[Spring_Boot]] — 框架实体
- [[摘要-spring-boot-知识库]] — 来源
- [[raw/09-archive/设计模式/raw/09-archive/Spring-boot]] — 原始素材
