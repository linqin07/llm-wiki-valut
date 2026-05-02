---
title: "SQL优化"
type: concept
tags: [性能, 索引, 查询优化]
sources: [raw/01-articles/mysql/优化/]
last_updated: 2026-05-01
---

## 定义

SQL 优化是通过分析和调整 SQL 语句、索引设计、表结构等方式来提高数据库查询性能的技术。

## 关键信息

### 索引优化原则

1. 避免全表扫描，优先在 WHERE、ORDER BY 涉及的列上建立索引
2. 索引不是越多越好，会降低 INSERT/UPDATE 效率
3. 一个表的索引数最好不要超过 6 个
4. 使用数字型字段优于字符型
5. 使用 VARCHAR 代替 CHAR

### 导致索引失效的场景

| 场景 | 说明 | 解决方案 |
|------|------|----------|
| NULL 值判断 | `WHERE num IS NULL` | 使用默认值代替 NULL |
| != 或 <> | 不等查询 | 改用 UNION ALL |
| OR 条件 | `WHERE num=10 OR num=20` | 改用 UNION ALL |
| IN/NOT IN | 可能导致全表扫描 | 连续值用 BETWEEN |
| 参数化查询 | `WHERE num=@num` | 使用 FORCE INDEX |
| 表达式操作 | `WHERE num/2=100` | 改为 `WHERE num=100*2` |
| 函数操作 | `WHERE SUBSTRING(name,1,3)='abc'` | 避免在索引列使用函数 |
| LIKE '%abc%' | 前缀通配符 | 使用 `LIKE 'abc%'` |

### EXPLAIN 执行计划

**type 字段（性能从优到差）：**

| 类型 | 说明 |
|------|------|
| system | 表只有一条记录 |
| const | 通过索引一次找到，用于主键或唯一索引 |
| eq_ref | 唯一性索引扫描 |
| ref | 非唯一性索引扫描 |
| range | 范围查询（BETWEEN、IN、>、<） |
| index | 全索引文件扫描 |
| all | 全表扫描（最差） |

**关键字段：**
- `possible_keys`：可能使用的索引
- `key`：实际使用的索引
- `key_len`：索引长度，越大越好
- `rows`：预估扫描行数，越小越好
- `Extra`：Using index 表示使用覆盖索引

### 多表 JOIN 优化

1. 先缩小范围再 JOIN，避免数据量直接相乘
2. 使用 EXISTS 替代直接 JOIN
3. 先过滤条件再连接

### 慢查询日志

```sql
-- 开启慢查询日志
SET GLOBAL slow_query_log=1;

-- 设置慢查询时间（秒）
SET GLOBAL long_query_time=1;

-- 查看慢查询配置
SHOW VARIABLES LIKE '%slow%';
```

### 常用 SQL 技巧

- CASE WHEN：条件表达式
- CONCAT/CONCAT_WS：字符串连接
- LOCATE/FIND_IN_SET：字符串查找
- DATE_FORMAT/DATE_SUB/DATE_ADD：日期处理

## 关联连接

- [[MySQL]] — 数据库系统
- [[InnoDB]] — 存储引擎
- [[B+树索引]] — 索引数据结构
- [[摘要-mysql-优化]] — 来源
