---
title: "ZooKeeper"
type: entity
tags: [分布式协调, Apache, 开源]
sources:
  - "[[摘要-zookeeper-知识体系]]"
  # 另有 5 个原始素材文件，详见关联连接
actionLink: "[[raw/09-archive/Linux/zookeeper/1.简介]]"
last_updated: 2026-05-02
---

## 定义
ZooKeeper 是分布式协调服务，提供分布式锁、配置维护、Master 选举等功能。

## 数据模型
- **Znode**：由 stat（状态）、data（数据，≤1M）、children（子节点）组成
- **临时节点**：生命周期依赖会话，不允许有子节点
- **永久节点**：持久存在
- **Watch 机制**：一次性触发器，触发后需重新注册

## 应用场景
- **Master 选举**：利用临时节点唯一性
- **命名服务**：利用顺序节点生成全局唯一 ID
- **分布式锁**：排它锁（临时子节点）和共享锁（临时顺序节点 + Watch）

## ACL 权限
四种模式：IP（精确/段匹配）、Digest（用户名密码）、World（开放）、Super（超级用户）。ACL 无继承性。

## Curator 客户端
提供超时自动重连、持久化 Watch、递归创建节点等增强功能。

## 关联连接
- [[Kafka]] — 依赖 ZooKeeper
- [[分布式锁]] — 应用场景
- [[摘要-zookeeper-知识体系]] — 来源
- [[raw/09-archive/Linux/zookeeper/1.简介]] — 原始素材
- [[raw/09-archive/Linux/zookeeper/2.下载安装zk]] — 原始素材
- [[raw/09-archive/Linux/zookeeper/3.zk命令]] — 原始素材
- [[raw/09-archive/Linux/zookeeper/4.原生API]] — 原始素材
- [[raw/09-archive/Linux/zookeeper/5.应用场景]] — 原始素材
- [[raw/09-archive/Linux/zookeeper/6.Apache Curator客户端API]] — 原始素材
