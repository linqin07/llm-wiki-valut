---
title: "外观模式（Facade Pattern）"
type: concept
tags: [设计模式, 结构型模式, Java, 简化接口]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/外观模式]]"
last_updated: 2026-05-01
---

## 定义

外观模式（Facade Pattern）是一种结构型设计模式，为子系统中的一组接口提供一个一致的界面。Facade 模式定义了一个高层接口，这个接口使得这一子系统更加容易使用。

**意图**：为子系统提供统一的高层接口。

**主要解决**：子系统复杂，需要简化接口。

**何时使用**：
- 当要为一个复杂子系统提供一个简单接口时
- 客户程序与抽象类的实现部分之间存在着很大的依赖性
- 当需要构建一个层次结构的子系统时

## 参与者

- **Facade**：知道哪些子系统类负责处理请求，将客户的请求代理给适当的子系统对象
- **Subsystem**：处理 Facade 对象指派的任务，没有 Facade 的任何相关信息

## 代码示例

**旧系统类：**

```java
public class ServiceA {
    public void methodA() {
        System.out.println("ServiceA");
    }
}

public class ServiceB {
    public void methodB() {
        System.out.println("ServiceB");
    }
}
```

**外观类（Facade）：**

```java
public class Facade {
    ServiceA a;
    ServiceB b;

    public Facade() {
        a = new ServiceA();
        b = new ServiceB();
    }

    public void methodA() {
        a.methodA();
        System.out.println("a顺便打下酱油");
    }

    public void methodB() {
        b.methodB();
        System.out.println("b顺便打下酱油");
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        Facade facade = new Facade();
        facade.methodA();
        System.out.println("-----------------");
        facade.methodB();
    }
}
```

## 应用场景

- 为复杂子系统提供简单接口
- 将客户与子系统分离
- 构建层次结构的子系统
- 数据库访问层
- 日志系统

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Adapter_Pattern]] — 适配器模式
- [[Decorator_Pattern]] — 装饰者模式
- [[Mediator_Pattern]] — 中介者模式
- [[raw/09-archive/设计模式/外观模式]] — 原始素材
