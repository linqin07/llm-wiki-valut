---
title: "装饰者模式（Decorator Pattern）"
type: concept
tags: [设计模式, 结构型模式, Java, 动态扩展]
sources:
  - raw/01-articles/设计模式/7.装饰者模式/
last_updated: 2026-05-01
---

## 定义

装饰者模式（Decorator Pattern）是一种结构型设计模式，动态地给一个对象添加一些额外的职责。就增加功能来说，Decorator 模式相比生成子类更为灵活。

**意图**：动态地给对象添加一些额外的属性或行为。

**主要解决**：需要扩展对象功能，但不改变其接口。

**何时使用**：
- 在不影响其他对象的情况下，以动态、透明的方式给单个对象添加职责
- 处理那些可以撤消的职责
- 当不能采用生成子类的方法进行扩充时

类似于 JDK 自带的 IO 流，很多就是使用这个模式。

## 参与者

- **Component**：定义一个对象接口，可以给这些对象动态地添加职责
- **ConcreteComponent**：定义一个对象，可以给这个对象添加一些职责
- **Decorator**：维持一个指向 Component 对象的指针，并定义一个与 Component 接口一致的接口
- **ConcreteDecorator**：向组件添加职责

## 代码示例

**组件接口（Component）：**

```java
public interface Person {
    void eat();
}
```

**具体组件（ConcreteComponent）：**

```java
public class Man implements Person {
    @Override
    public void eat() {
        System.out.println("男人在吃！");
    }
}
```

**抽象装饰者（Decorator）：**

```java
public abstract class Decorator implements Person {
    protected Person person;

    public Decorator(Person person) {
        this.person = person;
    }

    @Override
    public void eat() {
        person.eat();
    }
}
```

**具体装饰者（ConcreteDecorator）：**

```java
public class ManDecoratorA extends Decorator {
    public ManDecoratorA(Person person) {
        super(person);
    }

    @Override
    public void eat() {
        System.out.println("ManDecoratorA");
        super.eat();
    }
}

public class ManDecoratorB extends Decorator {
    public ManDecoratorB(Person person) {
        super(person);
    }

    @Override
    public void eat() {
        System.out.println("ManDecoratorB");
        super.eat();
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        Man man = new Man();
        Decorator decorator = new ManDecoratorA(new ManDecoratorB(man));
        decorator.eat();
    }
}
```

**输出：**

```
ManDecoratorA
ManDecoratorB
男人在吃！
```

## 应用场景

- 扩展类的功能
- 动态添加职责
- 替代继承
- Java IO 流

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Adapter_Pattern]] — 适配器模式
- [[Facade_Pattern]] — 外观模式
- [[Proxy_Pattern]] — 代理模式
