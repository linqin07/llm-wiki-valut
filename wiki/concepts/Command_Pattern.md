---
title: "命令模式（Command Pattern）"
type: concept
tags: [设计模式, 行为型模式, Java, 解耦, 撤销]
sources:
  - raw/01-articles/设计模式/14.命令模式/
last_updated: 2026-05-01
---

## 定义

命令模式（Command Pattern）是一种行为型设计模式，将一个请求封装为一个对象，从而使你可用不同的请求对客户进行参数化；对请求排队或记录请求日志，以及支持可撤消的操作。

**意图**：将请求封装为对象。

**主要解决**：需要将请求排队、记录日志或支持撤销。

**何时使用**：
- 抽象出待执行的动作以参数化某对象
- 在不同的时刻指定、排列和执行请求
- 支持取消操作
- 支持修改日志，这样当系统崩溃时，这些修改可以被重做一遍
- 用构建在原语操作上的高层操作构造一个系统

## 参与者

- **Command**：声明执行操作的接口
- **CommandImpl**：将一个接收者对象绑定于一个动作
- **Client**：创建一个具体命令对象并设定它的接收者
- **Invoker**：要求该命令执行这个请求
- **Receiver**：知道如何实施与执行一个请求相关的操作

## 代码示例

**命令抽象类：**

```java
public abstract class Command {
    protected Receiver receiver;

    public Command(Receiver receiver) {
        this.receiver = receiver;
    }

    public abstract void execute();
}
```

**具体命令：**

```java
public class CommandImpl extends Command {
    public CommandImpl(Receiver receiver) {
        super(receiver);
    }

    @Override
    public void execute() {
        receiver.receive();
    }
}
```

**接收者：**

```java
public class Receiver {
    public void receive() {
        System.out.println("This is Receive class!");
    }
}
```

**执行者：**

```java
public class Invoker {
    private Command command;

    public void setCommand(Command command) {
        this.command = command;
    }

    public void execute() {
        command.execute();
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        Receiver receiver = new Receiver();
        CommandImpl command = new CommandImpl(receiver);
        Invoker invoker = new Invoker();
        invoker.setCommand(command);
        invoker.execute();
    }
}
```

## 应用场景

- 撤销/重做功能
- 任务队列
- 日志记录
- 事务处理
- GUI 按钮点击

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Chain_of_Responsibility_Pattern]] — 责任链模式
- [[Memento_Pattern]] — 备忘录模式
- [[Observer_Pattern]] — 观察者模式
