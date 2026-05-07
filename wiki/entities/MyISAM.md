---
title: "MyISAM"
type: entity
tags: [存储引擎, MySQL, OLAP]
sources:
  - "[[摘要-mysql-技术内幕]]"
  - "[[摘要-mysql-基础知识]]"
actionLink: "[[raw/09-archive/mysql]]"
last_updated: 2026-05-01
---

## 定义

MyISAM 是 MySQL 的另一种存储引擎，不支持事务和行级锁，但支持全文索引。主要面向 OLAP（联机分析处理）场景，适合读多写少的应用。

## 关键信息

### 核心特性

- 不支持事务，每次查询具有原子性
- 表级锁设计
- 支持全文索引（InnoDB 不支持）
- 允许没有主键和索引的表存在
- 数据以文件形式存储，跨平台转移方便

### 与 InnoDB 的对比

| 特性 | MyISAM | InnoDB |
|------|--------|--------|
| 事务支持 | 不支持 | 支持 |
| 锁粒度 | 表级锁 | 行级锁 |
| 外键 | 不支持 | 支持 |
| 全文索引 | 支持 | 不支持 |
| 主键要求 | 允许无主键 | 自动生成 6 字节主键 |
| 可移植性 | 文件存储，方便迁移 | 需要 binlog 或 mysqldump |

### MERGE 存储引擎

MyISAM 支持 MERGE 存储引擎，可用于实现逻辑分表：
- 创建多个结构相同的子表
- 创建 MERGE 表统一查询
- INSERT_METHOD=LAST 指定插入位置

## 关联连接

- [[MySQL]] — 数据库系统
- [[InnoDB]] — 对比存储引擎
- [[分库分表]] — MERGE 引擎应用场景
- [[摘要-mysql-技术内幕]] — 来源
- [[摘要-mysql-基础知识]] — 来源
- [[raw/09-archive/mysql]] — 原始素材
