---
title: "InnoDB"
type: entity
tags: [存储引擎, MySQL, 事务, 行锁]
sources: [raw/01-articles/mysql/Mysql技术内幕.md]
last_updated: 2026-05-01
---

## 定义

InnoDB 是 MySQL 的默认存储引擎，支持事务、行级锁和外键。它通过多版本并发控制（MVCC）获得高并发性，实现了 SQL 标准的 4 种隔离级别（默认可重复读），主要面向 OLTP 场景。

## 关键信息

### 核心特性

- 支持事务，具有 ACID 特性
- 行级锁设计，支持高并发
- 支持外键约束
- 使用 MVCC 实现非锁定读
- 默认隔离级别：REPEATABLE READ

### 后台线程

| 线程 | 职责 |
|------|------|
| Master Thread | 核心线程，刷新脏页、合并插入缓冲、UNDO 页回收 |
| IO Thread | 处理 write、read、insert buffer、log 的 IO 操作 |
| Purge Thread | 回收已提交事务的 undo log |
| Page Cleaner Thread | 将脏页刷新操作独立执行，减轻 Master Thread 负担 |

### 内存管理

**缓冲池（Buffer Pool）**
- 查询时将页 FIX 在缓冲池中，下次读取相同页时直接从内存获取
- 修改时先修改缓冲池中的页，通过 Checkpoint 机制刷新到磁盘
- 缓存数据类型：索引页、数据页、undo 页、插入缓冲、自适应哈希索引等

**LRU List、Free List、Flush List**
- 使用优化后的 LRU 算法，中位插入策略（末尾 37%）
- 数据库启动时，LRU list 为空，页存放在 Free list 中
- 压缩页可减少空间、降低 IO

**重做日志缓存**
- 刷新时机：Master Thread 每秒、事务提交、日志缓存剩余空间小于一半

### Insert Buffer

- 物理页，数据结构为 B+ 树
- 针对非聚集索引的插入/更新操作
- 先判断非聚集索引页是否在缓冲池中，若不在则放入 Insert Buffer
- 以一定频率合并到辅助索引页，提高插入性能
- 缺点：宕机后恢复大量 Insert Buffer 需要较长时间

### Double Write（两次写）

- 解决脏页写入磁盘过程中宕机导致的数据损坏
- 写磁盘前先备份页的副本，失败由副本恢复
- 保证数据的可靠性

## 关联连接

- [[MySQL]] — 数据库系统
- [[MyISAM]] — 对比存储引擎
- [[ACID事务]] — 事务支持
- [[MVCC]] — 多版本并发控制
- [[B+树索引]] — 索引实现
- [[redo-log]] — 重做日志
- [[undo-log]] — 回滚日志
- [[摘要-mysql-技术内幕]] — 来源
