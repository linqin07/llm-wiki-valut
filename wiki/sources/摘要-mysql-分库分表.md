---
title: "摘要-mysql-分库分表"
type: source
tags: [MySQL, 分库分表, 分片, MERGE]
sources: [raw/01-articles/mysql/分库分表/]
last_updated: 2026-05-01
---

## 核心摘要

本文介绍 MySQL 分库分表的基本概念与实现方式。物理分表需要修改代码逻辑（如读写分离），逻辑分表通过中间件实现对应用透明的数据分片。文章还介绍了使用 MyISAM 的 MERGE 存储引擎实现逻辑分表的方案，通过创建多个子表并使用 MERGE 表统一查询，可以在不修改 SQL 的情况下实现数据分片。

## 关联连接

- [[MySQL]] — 数据库系统
- [[MyISAM]] — 存储引擎
- [[分库分表]] — 数据库分片策略
