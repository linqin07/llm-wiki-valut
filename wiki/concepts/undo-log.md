---
title: "undo-log"
type: concept
tags: [日志, 事务, 原子性, 回滚, MVCC]
sources:
  - "[[摘要-mysql-技术内幕]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/mysql]]"
last_updated: 2026-05-01
---

## 定义

undo log（回滚日志）是 InnoDB 存储引擎的逻辑日志，用于事务回滚和多版本并发控制（MVCC），保证事务的原子性。

## 关键信息

### 核心作用

- 保证事务的原子性（Atomicity）
- 支持事务回滚操作
- 实现 [[MVCC]] 多版本并发控制

### 工作原理

- 记录逻辑日志，每次执行 SQL 增加一条回滚语句
- INSERT → 记录 DELETE 的 undo log
- UPDATE → 记录反向 UPDATE 的 undo log
- DELETE → 记录 INSERT 的 undo log

### 存储结构

- 存储在 undo 表空间中
- 支持 undo 页的重用
- 通过 Purge Thread 回收已提交事务的 undo 页

### 崩溃恢复顺序

1. 先恢复 redo log
2. 再恢复 undo log

### 与 MVCC 的关系

- undo log 存储数据的旧版本
- 事务读取数据时，根据 ReadView 从 undo log 中获取可见版本
- 实现非锁定读，提高并发性能

## 关联连接

- [[MySQL]] — 数据库系统
- [[InnoDB]] — 实现存储引擎
- [[ACID事务]] — 保证原子性
- [[MVCC]] — 多版本并发控制
- [[redo-log]] — 重做日志
- [[binlog]] — 归档日志
- [[摘要-mysql-技术内幕]] — 来源
- [[摘要-mysql-分布式事务]] — 来源
