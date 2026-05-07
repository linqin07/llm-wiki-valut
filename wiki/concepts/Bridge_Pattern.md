---
title: "桥接模式（Bridge Pattern）"
type: concept
tags: [设计模式, 结构型模式, Java, 分离抽象]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/桥接模式]]"
last_updated: 2026-05-01
---

## 定义

桥接模式（Bridge Pattern）是一种结构型设计模式，将抽象部分与它的实现部分分离，使它们都可以独立地变化。

**意图**：将抽象部分与实现部分分离。

**主要解决**：抽象和实现需要独立变化。

**何时使用**：
- 不希望在抽象和它的实现部分之间有一个固定的绑定关系
- 类的抽象以及它的实现都应该可以通过生成子类的方法加以扩充
- 对一个抽象的实现部分的修改应对客户不产生影响
- 在多个对象间共享实现

## 参与者

- **Abstraction**：定义抽象类的接口，维护一个指向 Implementor 类型对象的指针
- **RefinedAbstraction**：扩充由 Abstraction 定义的接口
- **Implementor**：定义实现类的接口
- **ConcreteImplementor**：实现 Implementor 接口并定义它的具体实现

## 代码示例

**颜色接口（Implementor）：**

```java
public interface Color {
    void bePaint(String shape);
}
```

**具体颜色（ConcreteImplementor）：**

```java
public class White implements Color {
    @Override
    public void bePaint(String shape) {
        System.out.println("白色" + shape);
    }
}

public class Black implements Color {
    @Override
    public void bePaint(String shape) {
        System.out.println("黑色的" + shape);
    }
}

public class Gray implements Color {
    @Override
    public void bePaint(String shape) {
        System.out.println("灰色的" + shape);
    }
}
```

**形状抽象类（Abstraction）：**

```java
public abstract class Shape {
    protected Color color;
    abstract void draw();

    public void setColor(Color color) {
        this.color = color;
    }
}
```

**具体形状（RefinedAbstraction）：**

```java
public class Square extends Shape {
    @Override
    void draw() {
        color.bePaint("正方形");
    }
}

public class Rectangle extends Shape {
    @Override
    void draw() {
        this.color.bePaint("长方形");
    }
}

public class Circle extends Shape {
    @Override
    void draw() {
        color.bePaint("圆形");
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        Color white = new White();
        Color black = new Black();
        Color gray = new Gray();

        Shape shape = new Circle();
        shape.setColor(white);
        shape.draw();

        Shape square = new Square();
        square.setColor(black);
        square.draw();
        
        Shape rectangle = new Rectangle();
        rectangle.setColor(gray);
        rectangle.draw();
    }
}
```

**输出：**

```
白色圆形
黑色的正方形
灰色的长方形
```

## 应用场景

- 需要将抽象和实现分离
- 需要在运行时切换实现
- 需要扩展抽象和实现
- JDBC 驱动程序
- GUI 框架

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Adapter_Pattern]] — 适配器模式
- [[Abstract_Factory_Pattern]] — 抽象工厂模式
- [[raw/09-archive/设计模式/桥接模式]] — 原始素材
