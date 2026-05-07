---
title: "Oracle"
type: entity
tags: [数据库, RDBMS, 商业数据库]
sources:
  - "[[摘要-mysql-sql面试题]]"
actionLink: "[[raw/09-archive/mysql/Oracle试题]]"
last_updated: 2026-05-01
---

## 定义

Oracle Database 是全球领先的关系型数据库管理系统，由 Oracle 公司开发。它是企业级应用中最广泛使用的商业数据库之一，以其强大的性能、可靠性和丰富的功能著称。

## 关键信息

### 物理结构

Oracle 数据库包含以下物理组件：
- 数据文件（Data Files）
- 控制文件（Control Files）
- 重做日志文件（Redo Log Files）
- 口令文件（Password Files）
- 参数文件（Parameter Files）

### 逻辑结构

| 层级 | 说明 |
|------|------|
| DataBase | 数据库 |
| TableSpace | 表空间 |
| Segment | 段（一个表就是一个段） |
| Extent | 区（磁盘空间分配的最小单位） |
| Data Block | 数据块 |

### 后台核心进程

| 进程 | 职责 |
|------|------|
| SMON | 数据块管理，实例恢复 |
| PMON | 进程异常终止清理 |
| DBWn | 数据块写入 |
| CheckPoint | 检查点进程 |
| LGWR | 日志写入（log buffer → online redo file） |

### 启动过程

1. **Nomount 阶段**：启动实例，不加载数据库
2. **Mount 阶段**：加载数据库，不打开
3. **Open 阶段**：打开数据库，允许访问

### 常用函数

- `CEIL()` — 向上取整
- `FLOOR()` — 向下取整
- `ROUND()` — 四舍五入
- `TRUNC()` — 截断

### 分页实现

Oracle 使用 ROWNUM 实现分页，需要三层嵌套：

```sql
-- 查询第 2 页数据（每页 5 条）
SELECT * FROM (
    SELECT ROWNUM ru, AAA.* FROM (
        SELECT * FROM table_name
    ) AAA WHERE ROWNUM < 11
) WHERE ru > 5;
```

**为什么需要三层嵌套：**
1. 没有 ORDER BY 时，查询结果顺序不确定
2. ORDER BY 和 ROWNUM 同时使用时，Oracle 先赋值 ROWNUM 再排序
3. ROWNUM 不能使用 >(=) 判断

## 关联连接

- [[MySQL]] — 对比数据库系统
- [[ACID事务]] — 事务特性
- [[B+树索引]] — 索引实现
- [[数据库隔离级别]] — 隔离级别
- [[SQL优化]] — SQL 性能优化
- [[分库分表]] — 分片策略
- [[摘要-mysql-sql面试题]] — 来源
- [[raw/09-archive/mysql/Oracle试题]] — 原始素材
