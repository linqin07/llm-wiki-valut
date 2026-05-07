---
title: "享元模式（Flyweight Pattern）"
type: concept
tags: [设计模式, 结构型模式, Java, 性能优化, 缓存]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/享元模式]]"
last_updated: 2026-05-01
---

## 定义

享元模式（Flyweight Pattern）是一种结构型设计模式，运用共享技术有效地支持大量细粒度的对象。

**意图**：运用共享技术有效地支持大量细粒度的对象。

**主要解决**：在有大量对象时，有可能会造成内存溢出，我们把其中共同的部分抽象出来，如果有相同的业务请求，直接返回在内存中已有的对象，避免重新创建。

**何时使用**：
- 系统中有大量对象
- 这些对象消耗大量内存
- 这些对象的状态大部分可以外部化
- 这些对象可以按照内蕴状态分为很多组
- 系统不依赖于这些对象身份，这些对象是不可分辨的

## Java 中的应用

- **String**：如果有则返回，如果没有则创建一个字符串保存在字符串缓存池里面
- **Integer**：int 的默认值 -128~127 这个范围，超过就自动拆箱

## 参与者

- **Flyweight**：描述一个接口，通过这个接口 flyweight 可以接受并作用于外部状态
- **ConcreteFlyweight**：实现 Flyweight 接口，并为内部状态增加存储空间
- **UnsharedConcreteFlyweight**：并非所有的 Flyweight 子类都需要被共享
- **FlyweightFactory**：创建并管理 flyweight 对象，确保合理地共享 flyweight

## 代码示例

**享元接口：**

```java
public interface Flyweight {
    void action(int arg);
}
```

**具体享元：**

```java
public class FlyweightImpl implements Flyweight {
    @Override
    public void action(int arg) {
        System.out.println("参数值: " + arg);
    }
}
```

**享元工厂：**

```java
public class FlyweightFactory {
    private static Map flyweights = new HashMap();

    public FlyweightFactory(String arg) {
        flyweights.put(arg, new FlyweightImpl());
    }

    public static Flyweight getFlyweight(String key) {
        if (flyweights.get(key) == null) {
            flyweights.put(key, new FlyweightImpl());
        }
        return (Flyweight) flyweights.get(key);
    }

    public static int getSize() {
        return flyweights.size();
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        Flyweight fly1 = FlyweightFactory.getFlyweight("a");
        fly1.action(1);
        fly1.action(2);
        fly1.action(3);

        Flyweight fly2 = FlyweightFactory.getFlyweight("b");
        fly2.action(1);
        fly2.action(2);
        fly2.action(3);
    }
}
```

## 应用场景

- 字符串常量池
- 数据库连接池
- 线程池
- 缓存系统
- 游戏中的粒子系统

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Singleton_Pattern]] — 单例模式
- [[Factory_Pattern]] — 工厂模式
- [[raw/09-archive/设计模式/享元模式]] — 原始素材
