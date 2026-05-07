---
title: "单例模式（Singleton Pattern）"
type: concept
tags: [设计模式, 创建型模式, Java, 线程安全]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/单例模式]]"
last_updated: 2026-05-01
---

## 定义

单例模式（Singleton Pattern）是一种创建型设计模式，保证一个类仅有一个实例，并提供一个访问它的全局访问点。

**意图**：保证一个类仅有一个实例，并提供一个访问它的全局访问点。

**主要解决**：一个全局使用的类频繁地创建与销毁。

**何时使用**：当您想控制实例数目，节省系统资源的时候。

**关键代码**：构造函数是私有的。

## 实现方式

### 1. 饿汉式（线程安全）

类加载时就创建好了实例对象，线程安全。

```java
public class Singleton1 {
    private final static Singleton1 INSTANCE = new Singleton1();
    
    private Singleton1() {
    }

    public static Singleton1 getInstance() {
        return INSTANCE;
    }
}
```

**优点**：实现简单，线程安全
**缺点**：类加载时就创建，可能浪费资源

### 2. 懒汉式（非线程安全）

获取实例时判断是否为空，空就创建一个。有需要时再创建（懒）。

```java
public class Singleton2 {
    private static Singleton2 instance = null;
    
    private Singleton2() {}

    public Singleton2 getInstance() {
        if (instance == null) {
            instance = new Singleton2();
        }
        return instance;
    }
}
```

**优点**：延迟加载，节省资源
**缺点**：非线程安全，并发时可能会有多个实例

### 3. 双重校验锁（线程安全）

类似懒汉式，进行两次判断，并且有 `synchronized` 关键字保证线程安全。`volatile` 禁止指令重排。

```java
public class Singleton {
    private static volatile Singleton instance = null;

    private Singleton() {
    }

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

**为什么需要 `volatile`？**

当执行 `instance = new Singleton()` 时，CPU 会执行：
1. `memory = allocate()` 分配对象的内存空间
2. `ctorInstance()` 初始化对象
3. `instance = memory` 设置 instance 指向刚分配的内存

在多线程情况下，可能会发生指令重排序，导致问题。

**为什么需要第二次判断？**

假设同时 A、B 线程通过第一个 if，然后 A 获得锁创建对象完成，释放锁，B 会再次创建对象覆盖。加个判断可以防止。

## 应用场景

- 配置管理器
- 连接池
- 线程池
- 缓存
- 日志对象

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Factory_Pattern]] — 工厂模式
- [[Abstract_Factory_Pattern]] — 抽象工厂模式
- [[raw/09-archive/设计模式/单例模式]] — 原始素材
