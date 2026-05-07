---
title: "Kafka"
type: entity
tags: [消息队列, 分布式, Apache, 开源]
sources:
  - "[[摘要-kafka-知识体系]]"
  - "raw/09-archive/Linux/Kafka/"
  # 另有 6 个原始素材文件，详见关联连接
actionLink: "[[raw/09-archive/Linux/Kafka/kafka知识]]"
last_updated: 2026-05-02
---

## 定义
Apache Kafka 是分布式流处理平台，提供高吞吐、低延迟的消息发布订阅能力。

## 核心概念
- **分区（Partition）**：消息有序存储单元，消费者组内唯一消费者处理
- **消费者组**：消费者数量不能超过分区数
- **副本（Replication）**：数据冗余保证高可用
- **Segment**：分区内日志分段，默认 1GB

## 生产者
- acks=0 不等待、acks=1 等 Leader、acks=all 等所有副本
- max.in.flight.requests.per.connection=1 保证顺序
- 支持 snappy/gzip/lz4 压缩

## 消费者
- 重平衡期间所有消费者暂停消费
- session.timeout.ms 默认 3 秒，heartbeat.interval.ms 设为其 1/3
- 混合提交：正常异步、退出同步

## 零拷贝
通过 mmap 和 sendfile 减少数据拷贝次数，提升 I/O 性能。

## 关联连接
- [[ZooKeeper]] — 协调服务
- [[Elasticsearch]] — 数据存储
- [[Logstash]] — 数据处理
- [[摘要-kafka-知识体系]] — 来源
- [[raw/09-archive/Linux/Kafka/kafka常用命令]] — 原始素材
- [[raw/09-archive/Linux/Kafka/kafka知识]] — 原始素材
- [[raw/09-archive/Linux/Kafka/linux安装kafka]] — 原始素材
- [[raw/09-archive/Linux/Kafka/生产者]] — 原始素材
- [[raw/09-archive/Linux/Kafka/消费者]] — 原始素材
- [[raw/09-archive/Linux/Kafka/Kafka零拷贝]] — 原始素材
- [[raw/09-archive/Linux/Kafka/kafka监控]] — 原始素材
- [[raw/09-archive/Linux/Kafka/删除topic数据]] — 原始素材
