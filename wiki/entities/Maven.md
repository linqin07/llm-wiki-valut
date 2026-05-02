---
title: "Maven"
type: entity
tags: [构建工具, Java, 依赖管理, Apache]
sources: [raw/01-articles/Java学习/构建工具/Maven.md]
last_updated: 2026-05-02
---

## 定义
Apache Maven 是 Java 项目的构建和依赖管理工具，通过 POM 文件声明项目结构和依赖。

## 多模块构建
单独构建子项目 B：`mvn install -pl :B -am`（-pl 指定项目，-am 同时构建依赖项目）

## 依赖仲裁三原则
1. 路径最短优先
2. POM 中最先声明优先
3. 子 POM 覆写父 POM

## 私服部署
- 上传 JAR：`mvn deploy:deploy-file`
- Release 仓库只能上传一次不可覆盖
- SNAPSHOT 仓库的 JAR 名称必须包含 SNAPSHOT

## 依赖排查
`mvn dependency:tree` 查看依赖树

## 关联连接
- [[Nexus]] — Maven 私服
- [[Jenkins]] — CI/CD 集成
- 摘要-maven-使用 — 来源
- [[摘要-构建工具]] — 构建工具汇总
