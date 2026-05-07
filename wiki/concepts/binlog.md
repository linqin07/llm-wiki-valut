---
title: "binlog"
type: concept
tags: [日志, 主从复制, 数据恢复]
sources:
  - "[[摘要-mysql-技术内幕]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/mysql/Mysql技术内幕]]"
last_updated: 2026-05-01
---

## 定义

binlog（二进制日志/归档日志）是 MySQL Server 层的逻辑日志，记录所有数据库的修改操作，主要用于主从复制和数据恢复。

## 关键信息

### 核心作用

- 主从复制：从库通过读取主库的 binlog 实现数据同步
- 数据恢复：通过 mysqlbinlog 工具恢复数据

### 记录模式

| 模式 | 说明 | 优缺点 |
|------|------|--------|
| ROW | 记录每一行的操作 | 日志量大，但数据一致性最好 |
| STATEMENT | 只记录 SQL 语句 | 日志量小，但某些函数（如 NOW()）可能导致不一致 |
| MIXED | 混合模式 | 自动选择 ROW 或 STATEMENT |

### 相关参数

- `max_binlog_size`：每个 binlog 文件的最大大小
- `sync_binlog`：控制 binlog 的刷盘时机
  - 0：由操作系统决定
  - 1：每次事务都持久化（推荐）
  - N：每 N 个事务持久化

### 与 redo log 的区别

| 特性 | redo log | binlog |
|------|----------|--------|
| 所属层 | InnoDB 引擎 | MySQL Server 层 |
| 日志类型 | 物理日志 | 逻辑日志 |
| 写入方式 | 循环写 | 追加写 |
| 空间 | 固定大小 | 文件可切换 |
| 用途 | 崩溃恢复 | 主从复制、数据恢复 |

### 两阶段提交

1. 执行器生成 binlog 并写入磁盘
2. 执行器调用引擎提交事务接口
3. 引擎将 redo log 改为 commit 状态

保证 redo log 和 binlog 的一致性。

## 关联连接

- [[MySQL]] — 数据库系统
- [[InnoDB]] — 存储引擎
- [[redo-log]] — 重做日志
- [[undo-log]] — 回滚日志
- [[ACID事务]] — 事务日志
- [[摘要-mysql-技术内幕]] — 来源
- [[摘要-mysql-分布式事务]] — 来源
