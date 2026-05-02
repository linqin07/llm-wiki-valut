---
title: "redo-log"
type: concept
tags: [日志, 事务, 持久性, 崩溃恢复]
sources: [raw/01-articles/mysql/]
last_updated: 2026-05-01
---

## 定义

redo log（重做日志）是 InnoDB 存储引擎特有的物理日志，记录数据页的物理修改操作，保证事务的持久性和崩溃恢复能力（crash-safe）。

## 关键信息

### 核心作用

- 保证事务的持久性（Durability）
- 实现崩溃恢复（crash-safe）
- 避免内存中的脏数据直接写入数据表 IBD 文件

### 工作流程

1. 执行 SQL，写入数据到内存中的 redo log buffer
2. 根据刷盘规则写入磁盘 redo log
3. 数据库故障时通过 redo log 恢复到 IDB 文件

### 刷盘规则

| 触发条件 | 说明 |
|----------|------|
| 事务提交 | 默认规则（innodb_flush_log_at_trx_commit=1） |
| 每秒刷盘 | Master Thread 定时刷新 |
| 缓冲区满 | log buffer 占用内存达一定百分比 |
| 检查点 | 事务中存在检查点时 |

### 写入机制

- 采用循环写方式
- 包含两个指针：
  - **write pos**：记录当前写入位置
  - **check point**：负责擦除已刷盘的数据
- 两者之间的间隔代表可继续记录的空间

### LSN（Log Sequence Number）

- 日志的逻辑序列号
- 标记数据页的版本
- 用于 Checkpoint 机制判断数据是否需要刷新

### 与 binlog 的区别

| 特性 | redo log | binlog |
|------|----------|--------|
| 所属层 | InnoDB 引擎特有 | MySQL Server 层 |
| 日志类型 | 物理日志（记录数据页修改） | 逻辑日志（记录 SQL 原始逻辑） |
| 写入方式 | 循环写，空间固定 | 追加写，文件可切换 |
| 用途 | 崩溃恢复 | 主从复制、数据恢复 |

### 相关参数

- `innodb_flush_log_at_trx_commit`：设为 1 时，每次事务的 redo log 直接持久化到磁盘
- `innodb_log_buffer_size`：redo log 缓冲区大小
- `innodb_log_file_size`：redo log 文件大小

## 关联连接

- [[MySQL]] — 数据库系统
- [[InnoDB]] — 实现存储引擎
- [[ACID事务]] — 保证持久性
- [[undo-log]] — 回滚日志
- [[binlog]] — 归档日志
- [[摘要-mysql-技术内幕]] — 来源
- [[摘要-mysql-分布式事务]] — 来源
