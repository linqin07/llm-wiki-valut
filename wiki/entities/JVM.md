---
title: "JVM"
type: entity
tags: [Java, 虚拟机, 性能调优]
sources:
  - "[[摘要-jvm-体系结构]]"
  # 另有 2 个原始素材文件，详见关联连接
actionLink: "[[raw/09-archive/Java学习/JVM/Java虚拟机]]"
last_updated: 2026-05-02
---

## 定义
JVM（Java Virtual Machine）是 Java 程序的运行时环境，负责字节码执行、内存管理和垃圾回收。

## 内存结构
- **方法区**：线程共享，存静态/常量/方法（16-64MB）
- **Java 堆**：线程共享，存对象实例，分新生代（Eden+S0+S1）和老年代（比例 8:1:1）
- **Java 栈**：线程私有，栈帧含局部变量表/操作数栈/方法出口
- **本地方法栈**、**PC 寄存器**、**执行引擎**

## 垃圾回收
- **可达性分析**：以 GC Roots 为起点（栈局部变量/JNI 引用/静态属性/常量引用）
- **标记-清除**：有碎片问题
- **复制算法**：用于新生代（Eden:Survivor=8:1）
- **标记-整理**：用于老年代
- **四种引用**：强引用不回收、软引用内存不足回收、弱引用下次 GC 回收、虚引用仅用于回收通知

## 常用调优参数
- -Xms 初始堆、-Xmx 最大堆、-Xmn 年轻代（推荐堆的 3/8）
- -XX:MaxTenuringThreshold 晋升年龄阈值
- -XX:MaxGCPauseMillis 最大 GC 停顿时间

## 收集器选择
- **SerialGC**：串行
- **ParallelGC**：并行，吞吐量优先
- **CMS**：并发，响应时间优先
- **G1GC**：区域化收集

## 诊断工具
- **jstack**：线程堆栈分析，检测死锁
- **jmap**：堆内存 dump，对象直方图
- **jstat**：GC 统计监控

## 类加载器
Bootstrap → Extension → Application 三级，双亲委派模型保证父加载器优先加载。

## 关联连接
- [[Arthas]] — Java 诊断工具
- [[摘要-jvm-体系结构]] — 来源
- [[摘要-java-复习题]] — Java 面试复习
- [[摘要-java-基础知识]] — Java 基础
- [[摘要-jvm-体系结构]] — 来源摘要
- [[raw/09-archive/Java学习/JVM/Java虚拟机]] — 原始素材
- [[raw/09-archive/Java学习/JVM/JVM 参数]] — 原始素材
- [[raw/09-archive/Java学习/JVM/系统缓慢JVM排查]] — 原始素材
