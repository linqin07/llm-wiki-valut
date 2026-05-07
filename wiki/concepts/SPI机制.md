---
title: "SPI 机制"
type: concept
tags: [Java, 服务发现, JDK]
sources:
  - "[[摘要-java-基础知识]]"
actionLink: "[[raw/09-archive/Java学习/基础知识/3.SPI接口动态加载]]"
last_updated: 2026-05-02
---

## 定义
SPI（Service Provider Interface）是 JDK 内置的服务发现机制，通过 META-INF/services/ 目录配置实现动态加载。

## 使用步骤
1. 定义接口
2. 实现接口
3. 在 META-INF/services/ 创建配置文件（文件名为接口全限定名，内容为实现类）
4. ServiceLoader.load 加载

## 注意事项
- 实现类必须有无参构造方法
- 典型应用：JDBC 驱动加载、日志框架切换

## 关联连接
- [[MyBatis]] — JDBC 驱动加载使用 SPI
- [[函数式编程]] — ServiceLoader 配合 Lambda
- [[摘要-java-基础知识]] — 来源摘要
- [[raw/09-archive/Java学习/基础知识/3.SPI接口动态加载]] — 原始素材
