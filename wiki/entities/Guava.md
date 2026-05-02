---
title: "Guava"
type: entity
tags: [Java, Google, 工具库, 开源]
sources: [raw/01-articles/Java学习/常用工具类/Guava常用.md]
last_updated: 2026-05-02
---

## 定义
Guava 是 Google 开发的核心 Java 库，提供集合、缓存、并发、字符串处理等工具。

## 常用功能
- **Optional**：空值处理，fromNullable 等同 ofNullable，or 等同 orElseGet
- **不可变集合**：线程安全，不支持 null
- **Multiset**：可重复 Set，统计元素出现次数（如 HashMultiset）
- **Joiner/Splitter**：字符串拼接（可跳过 null）和拆分（可 trimResults）
- **Cache**：本地缓存，支持 expireAfterAccess/expireAfterWrite
- **集合运算**：Sets.difference/intersection/union

## 关联连接
- [[摘要-guava-常用]] — 来源
