---
title: "访问者模式（Visitor Pattern）"
type: concept
tags: [设计模式, 行为型模式, Java, 双分派]
sources:
  - raw/01-articles/设计模式/23.访问者模式/
last_updated: 2026-05-01
---

## 定义

访问者模式（Visitor Pattern）是一种行为型设计模式，表示一个作用于某对象结构中的各元素的操作。它使你可以在不改变各元素的类的前提下定义作用于这些元素的新操作。

**意图**：表示作用于对象结构的操作。

**主要解决**：需要对对象结构执行多种不相关操作。

**关键代码**：在数据基础类里面有一个方法接受访问者，将自身引用传入访问者。

**何时使用**：
- 对象结构中对象对应的类很少改变，但经常需要在此对象结构上定义新的操作
- 需要对一个对象结构中的对象进行很多不同的并且不相关的操作，而需要避免让这些操作"污染"这些对象的类

## 参与者

- **Visitor**：访问者，参数为指定的数据结构接口
- **ConcreteVisitor**：具体访问者，实现访问者接口
- **Element**：数据结构接口，提供一个访问者方法
- **ConcreteElement**：具体数据结构类，实现数据结构接口

## 代码示例

**数据结构接口：**

```java
public interface ComputerPart {
    void accept(ComputerPartVisitor computerPartVisitor);
}
```

**具体数据结构：**

```java
public class Keyboard implements ComputerPart {
    @Override
    public void accept(ComputerPartVisitor computerPartVisitor) {
        computerPartVisitor.visit(this);
    }
}

public class Monitor implements ComputerPart {
    @Override
    public void accept(ComputerPartVisitor computerPartVisitor) {
        computerPartVisitor.visit(this);
    }
}

public class Mouse implements ComputerPart {
    @Override
    public void accept(ComputerPartVisitor computerPartVisitor) {
        computerPartVisitor.visit(this);
    }
}
```

**访问者接口：**

```java
public interface ComputerPartVisitor {
    void visit(ComputerPart computerPart);
}
```

**具体访问者：**

```java
public class ComputerPartDisplayVisitor implements ComputerPartVisitor {
    @Override
    public void visit(ComputerPart computerPart) {
        System.out.println(computerPart.getClass().getName());
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        ComputerPart computer = new Computer();
        computer.accept(new ComputerPartDisplayVisitor());

        System.out.println("--------------");
        Mouse mouse = new Mouse();
        mouse.accept(new ComputerPartDisplayVisitor());
    }
}
```

## 应用场景

- 编译器的语法树遍历
- 文件系统操作
- XML 文档处理
- 对象结构的多种操作
- 反射机制

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Iterator_Pattern]] — 迭代器模式
- [[Composite_Pattern]] — 组合模式
- [[Interpreter_Pattern]] — 解释器模式
