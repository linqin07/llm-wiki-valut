---
title: "Tomcat"
type: entity
tags: [Web服务器, Java, Apache, 开源]
sources: [raw/01-articles/Java学习/IDEA学习/发布应用到 tomcat.md]
last_updated: 2026-05-02
---

## 定义
Apache Tomcat 是 Java Servlet 容器和 Web 服务器，用于部署 Java Web 应用。

## 部署模式
- **war 模式**：打包为 war 文件部署，不支持热部署
- **exploded 模式**：展开目录部署，支持热部署（推荐开发使用）

## IDEA 集成
通过项目设置（Ctrl+Shift+Alt+S）配置 artifacts，添加 exploded artifact 并设置发布路径。

## 关联连接
- [[IntelliJ_IDEA]] — IDE 集成部署
- [[spring-boot-deployment]] — Spring Boot 内嵌 Tomcat
- [[摘要-tomcat-部署]] — 来源
