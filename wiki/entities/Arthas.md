---
title: "Arthas"
type: entity
tags: [Java, 诊断工具, 阿里巴巴, 开源]
sources: [raw/01-articles/Java学习/Arthas 基础教程/Arthas 基础教程.md, raw/01-articles/Java学习/Arthas 基础教程/Thread.md, raw/01-articles/Java学习/Arthas 基础教程/热部署.md, raw/01-articles/Java学习/Arthas 基础教程/编译和反编译.md]
last_updated: 2026-05-02
---

## 定义
Arthas 是阿里巴巴开源的 Java 诊断工具，可在不修改代码、不重启应用的情况下实时诊断线上 Java 应用的问题。

## 核心命令
- **sc（Search Class）**：搜索已加载的类，支持通配符
- **sm（Search Method）**：搜索类的方法
- **watch**：观察方法的入参和返回值，`-x` 控制遍历深度，`-e` 仅异常时触发
- **trace**：查询服务调用耗时，展示完整调用链路，最耗时代码标红
- **thread**：查看线程信息和堆栈，`-n N` 显示最忙线程，`-b` 找阻塞线程
- **jad（Java Decompiler）**：反编译 JVM 中的字节码为 Java 源码
- **mc（Memory Compiler）**：内存编译 .java 文件生成 .class
- **redefine**：加载外部 .class 替换 JVM 中已加载的类，实现热部署

## 典型工作流
1. 用 sc 定位类 → sm 定位方法 → watch/trace 深度观察
2. 热更新：jad 反编译 → 修改源码 → mc 内存编译 → redefine 加载

## 线程诊断
- thread -b 仅支持 synchronized，不支持 java.util.concurrent.Lock
- CPU 占比统计基于采样间隔，默认 100ms，建议拉长到 5000ms 降低开销

## 热部署限制
- 不允许新增 field/method
- 正在运行的函数必须退出后才能生效
- redefine 后原来的类不能恢复

## 关联连接
- [[JVM]] — Arthas 运行在 JVM 之上
- [[摘要-arthas-基础教程]] — 来源
