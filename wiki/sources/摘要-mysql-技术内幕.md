---
title: "摘要-mysql-技术内幕"
type: source
tags: [MySQL, InnoDB, 数据库, 索引, 事务]
sources: [raw/01-articles/mysql/Mysql技术内幕.md]
last_updated: 2026-05-01
---

## 核心摘要

本文深入剖析 MySQL 的技术实现细节，重点介绍 InnoDB 存储引擎的架构设计。内容涵盖 MySQL 的体系结构、存储引擎对比（InnoDB 与 MyISAM）、InnoDB 的后台线程与内存管理机制（缓冲池、LRU 列表、Checkpoint 技术）、Insert Buffer 与 Double Write 机制、以及三种核心日志文件（binlog、redo log、undo log）的作用与区别。此外还详细讲解了 B+ 树索引的原理，包括聚集索引、辅助索引和联合索引的最左匹配原则。

## 关联连接

- [[MySQL]] — 数据库系统
- [[InnoDB]] — 存储引擎
- [[MyISAM]] — 存储引擎
- [[B+树索引]] — 索引数据结构
- [[redo-log]] — 重做日志
- [[undo-log]] — 回滚日志
- [[binlog]] — 归档日志
- [[MVCC]] — 多版本并发控制
