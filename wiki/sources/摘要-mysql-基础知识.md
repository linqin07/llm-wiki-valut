---
title: "摘要-mysql-基础知识"
type: source
tags: [MySQL, 基础, 事务, 锁, 日志]
sources:
  - "raw/09-archive/mysql/基础知识/"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/mysql/基础知识]]"
last_updated: 2026-05-01
---

## 核心摘要

本系列文章涵盖 MySQL 的基础知识体系，包括：MySQL 查询执行过程（连接器→查询缓存→分析器→优化器→执行器）、InnoDB 与 MyISAM 存储引擎的详细对比、SQL 模式配置（特别是 ONLY_FULL_GROUP_BY 的影响）、数据库事务的 ACID 特性与四种隔离级别（读未提交、读已提交、可重复读、串行化）、锁机制（表锁、行锁、间隙锁、临键锁）以及三种日志（redo log、undo log、binlog）的工作原理。

## 关联连接

- [[MySQL]] — 数据库系统
- [[InnoDB]] — 存储引擎
- [[MyISAM]] — 存储引擎
- [[ACID事务]] — 事务四大特性
- [[数据库隔离级别]] — 事务隔离级别
- [[redo-log]] — 重做日志
- [[undo-log]] — 回滚日志
- [[binlog]] — 归档日志
- [[MVCC]] — 多版本并发控制
- [[raw/09-archive/设计模式/raw/09-archive/mysql/基础知识]] — 原始素材
