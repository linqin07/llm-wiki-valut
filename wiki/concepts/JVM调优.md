---
title: "JVM 调优"
type: concept
tags: [Java, 性能优化, JVM]
sources:
  - "[[摘要-jvm-体系结构]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Java学习/JVM/JVM 参数]]"
last_updated: 2026-05-02
---

## 定义
JVM 调优是通过调整 JVM 参数和选择合适的垃圾收集器来优化 Java 应用性能的过程。

## 内存参数
- -Xms 初始堆、-Xmx 最大堆（建议设为物理内存的 80%）
- -Xmn 年轻代（推荐堆的 3/8）、-Xss 线程栈（默认 1M）
- -XX:NewRatio 年轻代/老年代比值、-XX:SurvivorRatio Eden/Survivor 比值
- -XX:MaxTenuringThreshold 晋升年龄阈值

## 收集器选择策略
- **响应时间优先**：年轻代设大减少 GC 频率，使用 CMS/G1
- **吞吐量优先**：年轻代可到 Gbit 级，使用 ParallelGC
- CMS 碎片整理：-XX:CMSFullGCsBeforeCompaction + -XX:+UseCMSCompactAtFullCollection

## 排查流程
1. 系统级：free -m（内存）、top -c（CPU）、df -h（磁盘）
2. 线程：top -Hp PID → jstack -l PID
3. 内存：jmap -dump → jmap -histo:live
4. GC：jstat -gcutil PID 1000

## 关联连接
- [[JVM]] — 虚拟机
- [[Arthas]] — 诊断工具
- [[摘要-jvm-体系结构]] — 来源摘要
- [[raw/09-archive/设计模式/raw/09-archive/Java学习/JVM/JVM 参数]] — 原始素材
- [[raw/09-archive/设计模式/raw/09-archive/Java学习/JVM/系统缓慢JVM排查]] — 原始素材
