---
title: "IntelliJ IDEA"
type: entity
tags: [IDE, Java, JetBrains, 开发工具]
sources: [raw/01-articles/Java学习/IDEA学习/IDEA好用插件.md, raw/01-articles/Java学习/IDEA学习/IDEA远程debug-jar.md, raw/01-articles/Java学习/IDEA学习/IDEA中使用 Debug .md, raw/01-articles/Java学习/IDEA学习/Lombok 的使用.md, raw/01-articles/Java学习/IDEA学习/发布应用到 tomcat.md]
last_updated: 2026-05-02
---

## 定义
IntelliJ IDEA 是 JetBrains 开发的 Java 集成开发环境，被广泛认为是最智能的 Java IDE。

## Debug 调试
- **快捷键**：Shift+F9 启动调试、F7 单步进入、F8 单步过、F9 跳转下一断点
- **高级功能**：条件断点、异常断点、断点回退（Drop Frame）
- **多线程调试**：默认阻塞级别 ALL，可在 View Breakpoints 中设为 Thread 模式

## 远程调试
使用 JVM 参数启动 jar：`java -Xdebug -Xrunjdwp:transport=dt_socket,address=5005,server=y,suspend=y -jar xxx.jar`

## 实用插件
- MyBatis Log Plugin：还原 SQL 日志（Ctrl+Shift+Alt+O）
- JRebel：热部署
- RestfulToolkit：RESTful 接口调试
- Alibaba Java Coding Guidelines：阿里代码规范

## 关联连接
- [[Lombok]] — 代码生成插件
- [[Tomcat]] — 应用服务器
- [[Git]] — 版本控制集成
- [[摘要-idea-使用]] — 来源
