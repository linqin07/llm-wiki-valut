---
title: "spring-boot-deployment"
type: concept
tags: [Spring Boot, 部署, 打包, Maven]
sources: [raw/01-articles/Spring-boot/spring-boot打包部署/]
last_updated: 2026-05-01
---

## 定义

部署与打包是 Spring Boot 应用程序发布到生产环境的过程，支持多种部署方式。

## 部署方式

### 1. 可执行 JAR 包
- Spring Boot 默认打包方式
- 内嵌 Tomcat/Jetty/Undertow 服务器
- 直接运行：`java -jar app.jar`

### 2. WAR 包部署
- 部署到外部 Tomcat 等 Servlet 容器
- 需要继承 `SpringBootServletInitializer`
- 配置 `spring-boot-starter-tomcat` 为 provided

### 3. Maven 插件部署
- `spring-boot-maven-plugin` 打包可执行 JAR
- `maven-deploy-plugin` 部署到私服
- 排除特定 JAR 依赖

## 配置参数

- `-Dfile.encoding=utf-8`：设置文件编码
- `-Dspring.profiles.active=local`：指定激活的配置文件

## 关联连接

- [[Spring_Boot]] — 框架实体
- [[spring-boot-multi-environment]] — 多环境配置
- [[摘要-spring-boot-知识库]] — 来源
