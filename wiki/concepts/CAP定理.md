---
title: "CAP定理"
type: concept
tags: [分布式系统, 理论基础, CAP]
sources: [raw/01-articles/SpringCloud/1.Eureka服务注册中心.md]
last_updated: 2026-05-01
---

## 定义

CAP 定理（CAP Theorem）是分布式系统领域的著名理论，指出在任何分布式系统中，以下三个特性最多只能同时满足两个：

- **C（Consistency，一致性）**：所有节点在同一时间看到相同的数据
- **A（Availability，可用性）**：每个请求都能在合理时间内获得非错误响应
- **P（Partition Tolerance，分区容错性）**：系统在网络分区故障时仍能继续运行

## 在服务注册中心中的体现

### AP 模型 — [[Eureka]]
- 优先保证可用性
- Eureka 节点之间是平等的，没有 Leader 选举
- 网络分区时，各节点仍可提供服务，但数据可能短暂不一致
- 适合对可用性要求高的场景

### CP 模型 — Zookeeper
- 优先保证一致性
- 通过 Paxos（ZAB）算法选举 Leader
- 写操作只向 Leader 节点写入，再同步到其他节点
- 网络分区时可能拒绝服务以保证数据一致
- 适合对数据一致性要求高的场景

## 选型建议

- 需要高可用、容忍短暂不一致 → 选择 AP（如 Eureka、Nacos AP 模式）
- 需要强一致性、可接受短暂不可用 → 选择 CP（如 Zookeeper、Consul）

## 关联连接
- [[服务注册中心]] — CAP 定理的核心应用场景
- [[Eureka]] — AP 模型实践
- [[Nacos]] — 支持 AP/CP 切换
- [[摘要-spring-cloud-微服务]] — 来源
