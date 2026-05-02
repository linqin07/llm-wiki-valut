---
title: "工厂模式（Factory Pattern）"
type: concept
tags: [设计模式, 创建型模式, Java]
sources:
  - raw/01-articles/设计模式/3.工厂模式/
last_updated: 2026-05-01
---

## 定义

工厂模式（Factory Pattern）是一种创建型设计模式，定义一个用于创建对象的接口，让子类决定实例化哪个类。

**意图**：定义一个用于创建对象的接口，让子类决定实例化哪个类。

**主要解决**：对象创建逻辑复杂或多变。

**何时使用**：当一个类不知道它所必须创建的对象的类的时候。

**关键代码**：创建过程在其子类中执行。

## 核心思想

工厂模式将对象的创建过程封装起来，客户端不需要知道具体的创建逻辑，只需要告诉工厂需要什么对象即可。

## 工厂模式的变体

### 1. 简单工厂（Simple Factory）

不是 GoF 的标准模式，但很常用。通过一个工厂类根据参数创建不同的对象。

```java
public class SimpleFactory {
    public static Product createProduct(String type) {
        if ("A".equals(type)) {
            return new ProductA();
        } else if ("B".equals(type)) {
            return new ProductB();
        }
        return null;
    }
}
```

### 2. 工厂方法（Factory Method）

定义创建对象的接口，让子类决定实例化哪个类。

```java
// 抽象工厂
public abstract class Factory {
    public abstract Product createProduct();
}

// 具体工厂
public class ConcreteFactoryA extends Factory {
    @Override
    public Product createProduct() {
        return new ProductA();
    }
}
```

## 应用场景

- 日志记录器
- 数据库连接
- 文件解析器
- 任何需要根据条件创建不同对象的场景

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Singleton_Pattern]] — 单例模式
- [[Abstract_Factory_Pattern]] — 抽象工厂模式
- [[Builder_Pattern]] — 建造者模式
