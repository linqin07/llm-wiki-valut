---
title: "synchronized 锁"
type: concept
tags: [Java, 并发, 线程同步]
sources: [raw/01-articles/Java学习/基础知识/4.synchronized.md]
last_updated: 2026-05-02
---

## 定义
synchronized 是 Java 内置的关键字，用于实现线程同步和互斥访问。

## 锁对象有效性（JMeter 验证）
- **有效**：锁 this（当前实例唯一）、锁 Class 对象（类对象唯一）、锁字符串常量（常量池唯一）、静态同步方法
- **无效**：锁传入参数或查询出的对象（每次查询都是新对象）

## 核心原则
锁对象必须是多线程共享的唯一对象。

## 关联连接
- [[JVM]] — 锁实现原理
- [[摘要-synchronized-验证]] — 来源
