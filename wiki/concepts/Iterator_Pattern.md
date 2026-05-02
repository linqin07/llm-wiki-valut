---
title: "迭代器模式（Iterator Pattern）"
type: concept
tags: [设计模式, 行为型模式, Java, 遍历, 集合]
sources:
  - raw/01-articles/设计模式/16.迭代器模式/
last_updated: 2026-05-01
---

## 定义

迭代器模式（Iterator Pattern）是一种行为型设计模式，提供一种方法顺序访问一个聚合对象中各个元素，而又无须暴露该对象的内部表示。

**意图**：提供顺序访问聚合对象元素的方法。

**主要解决**：需要遍历集合而不暴露其内部结构。

**何时使用**：
- 访问一个聚合对象的内容而无需暴露它的内部表示
- 支持对聚合对象的多种遍历
- 为遍历不同的聚合结构提供一个统一的接口（即支持多态迭代）

## 参与者

- **Iterator**：迭代器定义访问和遍历元素的接口
- **ConcreteIterator**：具体迭代器实现迭代器接口，对该聚合遍历时跟踪当前位置
- **Aggregate**：聚合定义创建相应迭代器对象的接口
- **ConcreteAggregate**：具体聚合实现创建相应迭代器的接口

## 代码示例

**迭代器接口：**

```java
public interface Iterator {
    Object next();
    void first();
    void last();
    boolean hasNext();
}
```

**聚合接口：**

```java
public interface List {
    Iterator iterator();
    Object get(int index);
    int getSize();
    void add(Object obj);
}
```

**迭代器实现：**

```java
public class IteratorImpl implements Iterator {
    private List list;
    private int index;

    public IteratorImpl(List list) {
        index = 0;
        this.list = list;
    }

    @Override
    public Object next() {
        Object obj = list.get(index);
        index++;
        return obj;
    }

    @Override
    public void first() {
        index = 0;
    }

    @Override
    public void last() {
        index = list.getSize() - 1;
    }

    @Override
    public boolean hasNext() {
        return index < list.getSize();
    }
}
```

**聚合实现：**

```java
public class ListImpl implements List {
    private Object[] list;
    private int index;
    private int size;

    public ListImpl() {
        index = 0;
        size = 0;
        list = new Object[100];
    }

    @Override
    public Iterator iterator() {
        return new IteratorImpl(this);
    }

    @Override
    public Object get(int index) {
        return list[index];
    }

    @Override
    public int getSize() {
        return this.size;
    }

    @Override
    public void add(Object obj) {
        list[index++] = obj;
        size++;
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        List list = new ListImpl();
        list.add(1);
        list.add(2);
        list.add(3);

        // 第一种迭代方式
        Iterator iterator = list.iterator();
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }

        // 第二种迭代
        for (int i = 0; i < list.getSize(); i++) {
            System.out.println(list.get(i));
        }
    }
}
```

## 应用场景

- Java Collection 的 Iterator
- 数据库结果集遍历
- 文件系统遍历
- 树形结构遍历

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Composite_Pattern]] — 组合模式
- [[Visitor_Pattern]] — 访问者模式
