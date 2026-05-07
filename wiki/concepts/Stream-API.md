---
title: "Stream API"
type: concept
tags: [Java8, 函数式编程, 数据流]
sources:
  - "[[摘要-jdk8-新特性]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Java学习/JDK8/Stream流]]"
last_updated: 2026-05-02
---

## 定义
Stream API 是 Java 8 引入的数据流处理接口，支持声明式、函数式的集合操作。

## 核心概念
- **衔接操作**（Intermediate）：filter、map、sorted，延迟执行
- **终止操作**（Terminal）：anyMatch、forEach、collect、count、reduce，触发计算
- Stream 不可复用，二次使用抛 IllegalStateException，用 Supplier\<Stream\> 解决

## 常用方法
- filter（Predicate）、sorted（Comparator）、map（转换）
- reduce（归约为单值）、flatMap（嵌套结构扁平化）
- IntStream.rangeClosed（闭区间）、IntStream.range（开区间）

## Collectors 收集器
- groupingBy 分组、toMap 转映射（需处理重复 key，value 不能为 null）
- joining 字符串拼接、partitioningBy 二分分组、counting 计数

## 关联连接
- [[函数式编程]] — 编程范式
- [[泛型]] — 类型参数化
- JDK8 — 版本特性
- [[摘要-jdk8-新特性]] — 来源摘要
- [[摘要-jdk8-新特性]] — JDK8 新特性汇总
- [[raw/09-archive/设计模式/raw/09-archive/Java学习/JDK8/Stream流]] — 原始素材
- [[raw/09-archive/设计模式/raw/09-archive/Java学习/JDK8/collect]] — 原始素材
