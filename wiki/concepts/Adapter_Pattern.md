---
title: "适配器模式（Adapter Pattern）"
type: concept
tags: [设计模式, 结构型模式, Java]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/适配器模式]]"
last_updated: 2026-05-01
---

## 定义

适配器模式（Adapter Pattern）是一种结构型设计模式，将一个类的接口转换成客户希望的另外一个接口。Adapter 模式使得原本由于接口不兼容而不能一起工作的那些类可以一起工作。

**意图**：将一个类的接口转换成客户希望的另外一个接口。

**主要解决**：接口不兼容的类需要协同工作。

**何时使用**：
- 使用一个已经存在的类，而它的接口不符合你的需求
- 创建一个可以复用的类，该类可以与其他不相关的类或不可预见的类协同工作
- 使用一些已经存在的子类，但是不可能对每一个都进行子类化以匹配它们的接口

## 参与者

- **Target**：定义客户使用的接口
- **Adapter**：将 Adaptee 接口转换成 Target 接口
- **Adaptee**：定义一个已经存在的接口，这个接口需要适配
- **Client**：通过 Target 接口使用 Adaptee

## 代码示例

**被适配的类（Adaptee）：**

```java
public class TypeC {
    public void request() {
        System.out.println("type-c 接口");
    }
}
```

**目标接口（Target）：**

```java
public interface Mobile {
    void charge();
}
```

**适配器（Adapter）：**

```java
public class Adapter extends TypeC implements Mobile {
    @Override
    public void charge() {
        super.request();
        System.out.println("充电");
    }
}
```

**客户端测试：**

```java
public class Client {
    public static void main(String[] args) {
        Mobile mobile = new Adapter();
        mobile.charge();
    }
}
```

## 应用场景

- 系统需要使用现有的类，而此类的接口不符合系统的需要
- 想建立一个可以重复使用的类，用于与一些彼此之间没有太大关联的一些类一起工作
- 在设计中，需要改变多个已有子类的接口，适配器模式可以对这些子类进行适配

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Decorator_Pattern]] — 装饰者模式
- [[Facade_Pattern]] — 外观模式
- [[Proxy_Pattern]] — 代理模式
- [[raw/09-archive/设计模式/适配器模式]] — 原始素材
