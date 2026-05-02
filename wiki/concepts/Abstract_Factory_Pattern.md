---
title: "抽象工厂模式（Abstract Factory Pattern）"
type: concept
tags: [设计模式, 创建型模式, Java]
sources:
  - raw/01-articles/设计模式/2.抽象工厂模式/
last_updated: 2026-05-01
---

## 定义

抽象工厂模式（Abstract Factory Pattern）是一种创建型设计模式，提供一个创建一系列相关或相互依赖对象的接口，而无需指定它们具体的类。

**意图**：提供一个创建一系列相关依赖对象的接口，而无需指定它们具体的类。

**主要解决**：需要创建一组相关的对象。

**何时使用**：系统的产品有多于一个的产品族，而系统只消费其中某一族的产品。

**关键代码**：在一个工厂里聚合多个同类产品。

## 核心思想

抽象工厂模式是工厂模式的升级版本。工厂方法模式针对的是一个产品等级结构，而抽象工厂模式针对的是多个产品等级结构。

## 应用场景

- GUI 工具包，需要支持多种操作系统（Windows、Mac、Linux）
- 数据库访问层，需要支持多种数据库（MySQL、PostgreSQL、Oracle）
- 游戏开发，需要支持多种主题（现代、未来、中世纪）

## 与工厂方法模式的区别

| 模式 | 关注点 | 产品数量 |
|------|--------|----------|
| [[Factory_Pattern]] | 一个产品等级结构 | 单个产品 |
| [[Abstract_Factory_Pattern]] | 多个产品等级结构 | 一系列相关产品 |

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Factory_Pattern]] — 工厂模式
- [[Singleton_Pattern]] — 单例模式
- [[Builder_Pattern]] — 建造者模式
