---
title: "Redis"
type: entity
tags: [Redis, 缓存, 数据库, NoSQL]
sources:
  - "[[摘要-redis-知识汇总]]"
  - "[[摘要-spring-boot-知识库]]"
actionLink: "[[raw/09-archive/Linux/Redis/Redis 知识汇总]]"
last_updated: 2026-05-02
---

## 定义

Redis 是开源的内存数据结构存储系统，可用作数据库、缓存和消息队列。支持字符串、哈希、列表、集合、有序集合等多种数据结构。

## 关键信息

- **高性能**：基于内存操作，读写速度极快
- **丰富数据结构**：String、Hash、List、Set、Sorted Set
- **持久化**：RDB 快照和 AOF 日志两种持久化方式
- **发布订阅**：支持 Pub/Sub 消息模式
- **事务**：MULTI/EXEC 事务支持
- **集群**：Redis Cluster 分布式集群方案

## Spring Boot 整合

- **依赖**：`spring-boot-starter-data-redis`
- **配置**：`spring.redis.host`、`spring.redis.port`
- **缓存注解**：`@Cacheable`、`@CachePut`、`@CacheEvict`
- **序列化**：配置 `RedisTemplate` 的序列化方式

## Cluster 集群搭建
- 16384 个哈希槽通过 cluster addslots 分配
- cluster replicate 主节点 ID 设置从节点
- 集群模式登录需加 -c 参数

## 高并发问题
- **缓存穿透**：布隆过滤器
- **缓存击穿**：分布式锁 / 动态 TTL
- **缓存雪崩**：保证高可用 + 限流

## 分布式锁
`set lock:key 1 nx ex 30` 实现原子操作。

## 关联连接

- [[摘要-spring-boot-知识库]] — Spring Boot 来源
- [[摘要-redis-知识汇总]] — Linux 运维来源
- [[Spring_Boot]] — 框架整合
- [[raw/09-archive/Spring-boot/spring-boot-redis]] — 原始素材
- [[raw/09-archive/Linux/Redis/Redis 知识汇总]] — 原始素材
