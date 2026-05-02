---
title: "摘要-mysql-分布式事务"
type: source
tags: [MySQL, 事务, 分布式事务, XA]
sources: [raw/01-articles/mysql/深入了解分布式事物.md]
last_updated: 2026-05-01
---

## 核心摘要

本文详细解析 MySQL 事务的底层实现机制，重点介绍三种核心日志：redo log（保证持久性，记录数据页物理修改）、undo log（保证原子性，记录逻辑回滚操作）、binlog（用于主从复制和数据恢复）。文章对比了 redo log 与 binlog 的本质区别，并通过事务执行流程图解说明了两阶段提交机制。最后介绍了 XA 分布式事务的实现原理，包括事务管理器和资源管理器的角色。

## 关联连接

- [[MySQL]] — 数据库系统
- [[InnoDB]] — 存储引擎
- [[redo-log]] — 重做日志
- [[undo-log]] — 回滚日志
- [[binlog]] — 归档日志
- [[ACID事务]] — 事务四大特性
- [[MVCC]] — 多版本并发控制
