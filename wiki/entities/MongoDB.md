---
title: "MongoDB"
type: entity
tags: [NoSQL, 文档数据库, 开源]
sources: [raw/01-articles/Linux/MongoDb/find.md, raw/01-articles/Linux/MongoDb/常用命令.md]
last_updated: 2026-05-02
---

## 定义
MongoDB 是面向文档的 NoSQL 数据库，以 BSON 格式存储数据，支持灵活的查询和聚合。

## 常用操作
- use 数据库名 创建/切换数据库（插入数据后才可见）
- find 查询支持条件匹配、字段投影、$gt/$or 操作符
- update 多条需加 {multi:true}
- aggregate $group 支持单字段和多字段分组
- mongoexport/mongoimport 导入导出 JSON

## MongoTemplate
通过 Criteria.andOperator 组合动态条件查询。

## 关联连接
- [[摘要-mongodb-使用]] — 来源
