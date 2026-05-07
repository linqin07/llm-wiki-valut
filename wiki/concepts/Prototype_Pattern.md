---
title: "原型模式（Prototype Pattern）"
type: concept
tags: [设计模式, 创建型模式, Java, 克隆]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/原型模式]]"
last_updated: 2026-05-01
---

## 定义

原型模式（Prototype Pattern）是一种创建型设计模式，用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象。

**意图**：复制原型创建新对象。

**主要解决**：创建对象成本高，需要相似对象。

**何时使用**：
- 当一个系统应该独立于它的产品创建、构成和表示时
- 当要实例化的类是在运行时刻指定时
- 为了避免创建一个与产品类层次平行的工厂类层次时
- 当一个类的实例只能有几个不同状态组合中的一种时

## 参与者

- **Prototype**：声明一个克隆自身的接口
- **ConcretePrototype**：实现一个克隆自身的操作
- **Client**：让一个原型克隆自身从而创建一个新的对象

## 代码示例

```java
public class Prototype implements Cloneable {
    private String name;

    public Prototype(String name) {
        this.name = name;
    }

    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();
    }

    public String getName() {
        return name;
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) throws CloneNotSupportedException {
        Prototype prototype = new Prototype("sb");
        Prototype clone = (Prototype) prototype.clone();
        System.out.println(prototype.toString() + prototype.getName());
        System.out.println(clone.toString() + clone.getName());
    }
}
```

**输出：**

```
Prototype@4554617c sb
Prototype@74a14482 sb
```

## 浅克隆 vs 深克隆

| 类型 | 说明 | 场景 |
|------|------|------|
| 浅克隆 | 只复制基本类型字段，引用类型字段复制引用 | 对象没有引用类型字段 |
| 深克隆 | 完全复制对象，包括引用类型字段 | 对象包含引用类型字段 |

## 应用场景

- 创建对象成本高（如数据库连接）
- 需要大量相似对象
- 对象初始化复杂
- 避免创建工厂类层次

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Factory_Pattern]] — 工厂模式
- [[Abstract_Factory_Pattern]] — 抽象工厂模式
- [[Builder_Pattern]] — 建造者模式
- [[raw/09-archive/设计模式/原型模式]] — 原始素材
