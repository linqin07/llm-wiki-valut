---
title: "观察者模式（Observer Pattern）"
type: concept
tags: [设计模式, 行为型模式, Java, 事件驱动, 发布订阅]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/观察者模式]]"
last_updated: 2026-05-01
---

## 定义

观察者模式（Observer Pattern）是一种行为型设计模式，定义对象间的一种一对多的依赖关系，当一个对象的状态发生改变时，所有依赖于它的对象都得到通知并被自动更新。

**意图**：定义一对多的依赖关系。

**主要解决**：一个对象状态改变需要通知多个对象。

## 实现方式

### 1. 接口实现

**观察者接口：**

```java
public interface ReadMessage {
    void read();
}
```

**具体观察者：**

```java
public class User implements ReadMessage {
    private String message;
    private String name;

    public User(String name) {
        this.name = name;
    }

    @Override
    public void read() {
        System.out.println(name + " 接收到消息：" + message);
    }
}
```

**被观察者接口：**

```java
public interface Observer {
    void register(User user);
    void remove(User user);
    void notifyUser(String message);
}
```

**具体被观察者：**

```java
public class Server implements Observer {
    private List<User> userList = new ArrayList<>();

    @Override
    public void register(User user) {
        userList.add(user);
        System.out.println(user.getName() + "订阅");
    }

    @Override
    public void remove(User user) {
        userList.remove(user);
        System.out.println(user.getName() + "取消订阅");
    }

    @Override
    public void notifyUser(String message) {
        if (userList.size() == 0) return;
        userList.forEach(item -> {
            item.setMessage(message);
            item.read();
        });
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        User zhangshan = new User("zhangshan");
        User lisi = new User("lisi");
        User wangwu = new User("wangwu");

        Observer observer = new Server();
        observer.register(lisi);
        observer.register(zhangshan);

        observer.notifyUser("开饭拉");

        observer.remove(lisi);
        observer.register(wangwu);
        observer.notifyUser("收到转账100w元");
    }
}
```

**输出：**

```
lisi订阅
zhangshan订阅

lisi 接收到消息：开饭拉
zhangshan 接收到消息：开饭拉

lisi取消订阅
wangwu订阅

zhangshan 接收到消息：收到转账100w元
wangwu 接收到消息：收到转账100w元
```

### 2. Guava EventBus 实现

使用 Google Guava 库的 EventBus，简化事件发布和订阅。

### 3. Spring Event 实现

使用 Spring 框架的事件机制，通过 `ApplicationEvent` 和 `ApplicationListener` 实现。

## 应用场景

- 事件监听器
- 消息订阅系统
- GUI 事件处理
- Spring 事件机制
- RxJava 响应式编程

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Mediator_Pattern]] — 中介者模式
- [[State_Pattern]] — 状态模式
- [[Strategy_Pattern]] — 策略模式
- [[raw/09-archive/设计模式/观察者模式]] — 原始素材
