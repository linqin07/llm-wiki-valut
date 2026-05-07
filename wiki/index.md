# Wiki Index

## 设计模式（Design Patterns）

### 总览
- [[Design_Patterns]] — GoF 设计模式总览：23 种经典设计模式分类与选择指南
- [[摘要-design-patterns-java]] — 设计模式 Java 实现来源摘要

### 创建型模式（Creational Patterns）
- [[Singleton_Pattern]] — 单例模式：保证一个类仅有一个实例
- [[Factory_Pattern]] — 工厂模式：定义创建对象的接口
- [[Abstract_Factory_Pattern]] — 抽象工厂模式：创建一系列相关对象的接口
- [[Builder_Pattern]] — 建造者模式：复杂对象的构建与表示分离
- [[Prototype_Pattern]] — 原型模式：通过复制原型创建新对象

### 结构型模式（Structural Patterns）
- [[Adapter_Pattern]] — 适配器模式：接口转换
- [[Decorator_Pattern]] — 装饰者模式：动态添加职责
- [[Facade_Pattern]] — 外观模式：统一高层接口
- [[Bridge_Pattern]] — 桥接模式：抽象与实现分离
- [[Proxy_Pattern]] — 代理模式：控制对象访问
- [[Composite_Pattern]] — 组合模式：树形结构表示
- [[Flyweight_Pattern]] — 享元模式：共享细粒度对象

### 行为型模式（Behavioral Patterns）
- [[Command_Pattern]] — 命令模式：请求封装为对象
- [[Interpreter_Pattern]] — 解释器模式：语言文法表示
- [[Iterator_Pattern]] — 迭代器模式：顺序访问聚合对象
- [[Mediator_Pattern]] — 中介者模式：封装对象交互
- [[Memento_Pattern]] — 备忘录模式：保存和恢复对象状态
- [[Observer_Pattern]] — 观察者模式：一对多依赖关系
- [[State_Pattern]] — 状态模式：对象行为随状态改变
- [[Strategy_Pattern]] — 策略模式：算法族封装
- [[Template_Method_Pattern]] — 模板方法模式：算法骨架定义
- [[Chain_of_Responsibility_Pattern]] — 责任链模式：请求沿链传递直到被处理
- [[Visitor_Pattern]] — 访问者模式：作用于对象结构的操作

---

## 数据库（Database）

### 实体
- [[MySQL]] — 最流行的开源关系型数据库管理系统
- [[InnoDB]] — MySQL 默认事务型存储引擎
- [[MyISAM]] — MySQL 的 OLAP 存储引擎
- [[Oracle]] — 企业级商业关系型数据库

### 概念
- [[ACID事务]] — 数据库事务的四大特性（原子性、一致性、隔离性、持久性）
- [[MVCC]] — 多版本并发控制机制
- [[B+树索引]] — InnoDB 索引数据结构
- [[redo-log]] — InnoDB 重做日志，保证持久性
- [[undo-log]] — InnoDB 回滚日志，保证原子性
- [[binlog]] — MySQL 归档日志，用于主从复制
- [[数据库隔离级别]] — 事务隔离级别定义
- [[SQL优化]] — SQL 性能优化方法
- [[分库分表]] — 数据库分片策略

### 来源
- [[摘要-mysql-技术内幕]] — MySQL 技术实现深度解析
- [[摘要-mysql-分布式事务]] — MySQL 事务与分布式事务机制
- [[摘要-mysql-基础知识]] — MySQL 基础知识体系
- [[摘要-mysql-安装]] — MySQL 安装与配置指南
- [[摘要-mysql-优化]] — MySQL 性能优化实践
- [[摘要-mysql-分库分表]] — MySQL 分库分表方案
- [[摘要-mysql-sql面试题]] — SQL 面试题与 LeetCode 解答

---

## Spring Boot

### 实体
- [[Spring_Boot]] — 快速开发脚手架，简化 Spring 应用配置和部署
- [[GraphQL]] — API 查询语言，支持客户端精确指定数据结构
- [[MyBatis]] — 优秀持久层框架，支持定制化 SQL 和高级映射
- [[MyBatis_Plus]] — MyBatis 增强工具，内置通用 CRUD 和代码生成
- [[Druid]] — 阿里巴巴开源数据库连接池，内置监控和防火墙
- [[Swagger]] — API 文档自动生成和测试工具
- [[Thymeleaf]] — 现代化服务器端模板引擎
- [[Spring_Security]] — Spring 安全框架，提供认证和授权
- [[WebSocket]] — 全双工实时通信协议
- [[JPA]] — Java 持久化规范，定义 ORM 标准 API
- [[MapStruct]] — 编译时类型安全 Bean 映射框架
- [[Redis]] — 内存数据结构存储，用作缓存和消息队列

### 概念
- [[spring-boot-auto-configuration]] — 根据依赖和配置自动装配 Bean
- [[spring-boot-aop]] — 面向切面编程，分离横切关注点
- [[spring-boot-exception-handler]] — 全局异常处理机制
- [[spring-boot-interceptor]] — Spring MVC 请求拦截器
- [[spring-boot-json]] — JSON 序列化与反序列化处理
- [[spring-boot-logback]] — Logback 日志框架配置
- [[spring-boot-scheduled-tasks]] — 定时任务多种实现方式
- [[spring-boot-deployment]] — 应用打包与部署方案
- [[spring-boot-multi-environment]] — 多环境配置管理

### 来源
- [[摘要-spring-boot-知识库]] — Spring Boot 技术知识库综合摘要
- [[摘要-spring-mvc-实践]] — Spring MVC 统一日志/拦截器/入参/异常/出参处理
- [[摘要-spring-技术点]] — Spring Bean 生命周期/事务/嵌套失效分析

---

## Spring Cloud

### 实体
- [[Eureka]] — Netflix 服务注册中心，基于 AP 原则构建
- [[Nacos]] — 阿里巴巴服务治理组件，同时支持配置管理和服务发现
- [[Spring_Cloud_Gateway]] — 新一代 API 网关，基于 WebFlux 构建
- [[Zuul]] — Netflix API 网关，提供动态路由和过滤功能
- [[Feign]] — 声明式 HTTP 客户端，简化微服务间远程调用

### 概念
- [[服务注册中心]] — 微服务架构中的服务注册与发现基础设施
- [[服务网关]] — 微服务统一入口，承担路由、认证、限流等横切关注点
- [[CAP定理]] — 分布式系统中一致性、可用性、分区容错性的权衡理论

### 来源
- [[摘要-spring-cloud-微服务]] — Spring Cloud 微服务体系核心组件实践笔记

---

## Java 工具与框架

### 实体
- [[Arthas]] — 阿里巴巴开源 Java 诊断工具
- [[Git]] — 分布式版本控制系统
- [[GitLab]] — 自托管 DevOps 平台
- [[IntelliJ_IDEA]] — JetBrains Java 集成开发环境
- [[Lombok]] — Java 代码生成库
- [[Tomcat]] — Java Servlet 容器
- [[Netty]] — 异步事件驱动网络框架
- [[Akka]] — Actor 模型事件驱动框架
- [[SkyWalking]] — Apache 分布式追踪 APM 系统
- [[Jenkins]] — 开源 CI/CD 自动化服务器
- [[JHipster]] — 全栈 Web 应用代码生成器
- [[Maven]] — Java 构建和依赖管理工具
- [[Nexus]] — 制品仓库管理器
- [[Guava]] — Google 核心 Java 工具库
- [[OkHttp3]] — Square HTTP 客户端
- [[JVM]] — Java 虚拟机

### 概念
- [[Stream-API]] — Java 8 数据流处理接口
- [[函数式编程]] — Lambda 与函数式接口
- [[JVM调优]] — JVM 参数调整与性能优化
- [[synchronized锁]] — Java 内置线程同步关键字
- [[泛型]] — Java 类型参数化机制
- [[SPI机制]] — JDK 服务发现机制
- [[正则表达式]] — 文本模式匹配语言

### 来源
- [[摘要-arthas-基础教程]] — Arthas 命令与热更新
- [[摘要-git-使用]] — Git 命令与 IDEA 集成
- [[摘要-gitlab-安装维护]] — GitLab 安装与运维
- [[摘要-idea-使用]] — IDEA 调试与插件
- [[摘要-jdk8-新特性]] — Stream/函数式/时间API
- [[摘要-jvm-体系结构]] — JVM 内存/GC/调优/排查
- [[摘要-java-基础知识]] — 基础语法与并发
- [[摘要-java-工具类]] — Guava/MapStruct/OkHttp
- [[摘要-netty-实战]] — Netty 与 Akka 框架
- [[摘要-skywalking-源码调试]] — 分布式追踪概念
- [[摘要-构建工具]] — Jenkins/JHipster/Maven
- [[摘要-java-解决方案]] — SSE/文档转换/连接池
- [[摘要-正则表达式]] — 正则语法完整教程

---

## 中间件（Middleware）

### 实体
- [[Docker]] — 容器化平台
- [[Elasticsearch]] — 分布式全文搜索引擎
- [[Kafka]] — 分布式流处理平台
- [[ZooKeeper]] — 分布式协调服务
- [[Nginx]] — 高性能反向代理服务器
- [[MongoDB]] — 文档型 NoSQL 数据库

### 来源
- [[摘要-docker-使用]] — Docker 安装/用法/Compose
- [[摘要-elasticsearch-运维]] — ES 架构/索引/运维/优化
- [[摘要-kafka-知识体系]] — Kafka 概念/生产者/消费者/零拷贝
- [[摘要-zookeeper-知识体系]] — ZK 数据模型/选举/分布式锁
- [[摘要-nginx-配置]] — Nginx 安装/负载均衡/反向代理
- [[摘要-elk-其他组件]] — Logstash/Metricbeat
- [[摘要-mongodb-使用]] — MongoDB 查询与聚合
- [[摘要-redis-知识汇总]] — Redis 集群/缓存问题/分布式锁

---

## Linux 运维

### 来源
- [[摘要-linux-系统运维]] — 文件权限/查找/压缩/网络/定时任务/防火墙
- [[摘要-linux-shell-脚本]] — Shell 变量/awk/sed/if 条件

---

## AI 与大模型

### 概念
- [[Prompt_Engineering]] — 提示工程：设计和优化 LLM 输入提示的技术学科

### 来源
- [[摘要-llm-应用开发]] — AI 产品架构与 Prompt Engineering

---

## 数据结构与算法

### 来源
- [[摘要-数据结构]] — BitMap 位图与 B+树索引

---

## 面试复习

### 来源
- [[摘要-java-复习题]] — Java 基础/网络/多线程/面试题

---

## Python

### 来源
- [[摘要-python-环境配置]] — conda/pip/Poetry 环境管理

---

*最后更新：2026-05-02*
