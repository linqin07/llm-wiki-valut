---
title: "Elasticsearch"
type: entity
tags: [搜索引擎, ELK, 分布式, 开源]
sources: [raw/01-articles/Linux/ELK/ES/1.认识.md, raw/01-articles/Linux/ELK/ES/2.倒排索引.md, raw/01-articles/Linux/ELK/ES/3.索引模板.md, raw/01-articles/Linux/ELK/ES/4.安装.md, raw/01-articles/Linux/ELK/ES/5.ES数据冷热分离.md, raw/01-articles/Linux/ELK/ES/6.数据分片迁移.md, raw/01-articles/Linux/ELK/ES/7.常用命令.md, raw/01-articles/Linux/ELK/ES/8.快照和恢复.md, raw/01-articles/Linux/ELK/ES/9.x-pack插件.md, raw/01-articles/Linux/ELK/ES/10.常用api.md, raw/01-articles/Linux/ELK/ES/11.优化.md, raw/01-articles/Linux/ELK/ES/12.es-sql.md]
last_updated: 2026-05-02
---

## 定义
Elasticsearch 是分布式全文搜索引擎，基于倒排索引实现高性能检索，是 ELK Stack 的核心组件。

## 架构
- **集群健康状态**：green（全部可用）、yellow（主分片可用，副本不全）、red（主分片不全）
- **节点类型**：主节点、数据节点、协调节点
- **分片**：主分片 + 副本分片，总分片数不超 1.3 万

## 数据写入流程
hash(document_id) % num_primary_shards → 写入 translog + 内存缓冲 → 1 秒刷新可搜索 → 30 分钟或 translog 过大时 flush 刷盘

## 运维要点
- 不能用 root 启动，需专用用户
- JVM 堆内存不超 32G（配 31G），推荐 G1GC
- 单分片大小控制在 30GB
- 磁盘水位线：low 85%、high 90%、flood_stage 95%（强制只读）
- 冷热分离：node.attr.box_type 标签 + 路由分配策略

## 关联连接
- [[Logstash]] — 数据处理
- [[Kibana]] — 可视化
- [[Kafka]] — 数据管道
- [[摘要-elasticsearch-运维]] — 来源
