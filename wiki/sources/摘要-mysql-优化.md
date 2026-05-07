---
title: "摘要-mysql-优化"
type: source
tags: [MySQL, 优化, 索引, explain, 慢查询]
sources:
  - "raw/09-archive/mysql/优化/"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/mysql/优化]]"
last_updated: 2026-05-01
---

## 核心摘要

本系列文章聚焦 MySQL 性能优化实践，涵盖：索引设计原则与最左匹配原则、explain 执行计划详解（type 字段从 system 到 all 的性能排序）、导致索引失效的常见场景（null 判断、!=、or、函数操作等）、多表 JOIN 优化策略（使用 EXISTS 替代直接 JOIN）、慢查询日志配置与分析方法，以及常用 SQL 技巧（case when、日期函数、字符串处理等）。

## 关联连接

- [[MySQL]] — 数据库系统
- [[InnoDB]] — 存储引擎
- [[B+树索引]] — 索引数据结构
- [[SQL优化]] — SQL 优化方法
- [[raw/09-archive/设计模式/raw/09-archive/mysql/优化]] — 原始素材
