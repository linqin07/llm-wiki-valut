---
title: "中介者模式（Mediator Pattern）"
type: concept
tags: [设计模式, 行为型模式, Java, 解耦, 中介]
sources:
  - raw/01-articles/设计模式/17.中介者模式/
last_updated: 2026-05-01
---

## 定义

中介者模式（Mediator Pattern）是一种行为型设计模式，用一个中介对象来封装一系列的对象交互。中介者使各对象不需要显式地相互引用，从而使其耦合松散，而且可以独立地改变它们之间的交互。

**意图**：用中介对象封装一系列对象交互。

**主要解决**：对象之间存在复杂的直接依赖关系。

**何时使用**：
- 一组对象以定义良好但是复杂的方式进行通信，产生的相互依赖关系结构混乱且难以理解
- 一个对象引用其他很多对象并且直接与这些对象通信，导致难以复用该对象
- 定制一个分布在多个类中的行为，而又不想生成太多的子类

## 参与者

- **Mediator**：中介者定义一个接口用于与各同事（Colleague）对象通信
- **ConcreteMediator**：具体中介者通过协调各同事对象实现协作行为，了解并维护它的各个同事
- **Colleague**：每一个同事类都知道它的中介者对象，在需与其他同事通信的时候，与它的中介者通信

## 代码示例

**中介者抽象类：**

```java
public abstract class Mediator {
    public abstract void notice(String content);
}
```

**具体中介者：**

```java
public class ConcreteMediator extends Mediator {
    private ColleagueA ca;
    private ColleagueB cb;

    public ConcreteMediator() {
        ca = new ColleagueA();
        cb = new ColleagueB();
    }

    @Override
    public void notice(String content) {
        if (content.equals("boss")) {
            ca.action();
        }
        if (content.equals("client")) {
            cb.action();
        }
    }
}
```

**同事抽象类：**

```java
public abstract class Colleague {
    abstract void action();
}
```

**具体同事：**

```java
public class ColleagueA extends Colleague {
    @Override
    void action() {
        System.out.println("A 努力工作");
    }
}

public class ColleagueB extends Colleague {
    @Override
    void action() {
        System.out.println("B 努力工作");
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        ConcreteMediator concreteMediator = new ConcreteMediator();
        concreteMediator.notice("boss");
        concreteMediator.notice("client");
    }
}
```

**输出：**

```
A 努力工作
B 努力工作
```

## 应用场景

- 聊天室
- GUI 框架（MVC 中的 Controller）
- 航空管制系统
- 中介平台

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Facade_Pattern]] — 外观模式
- [[Observer_Pattern]] — 观察者模式
