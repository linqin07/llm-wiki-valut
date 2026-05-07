---
title: 状态模式（State Pattern）
type: concept
tags:
  - 设计模式
  - 行为型模式
  - Java
  - 状态机
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/Chain_of_Responsibility_Pattern]]"
last_updated: 2026-05-01
---

## 定义

状态模式（State Pattern）是一种行为型设计模式，允许一个对象在其内部状态改变时改变它的行为。对象看起来似乎修改了它的类。

**意图**：允许对象在内部状态改变时改变行为。

**主要解决**：对象行为取决于其状态。

**何时使用**：
- 一个对象的行为取决于它的状态，并且它必须在运行时刻根据状态改变它的行为
- 一个操作中含有庞大的多分支的条件语句，且这些分支依赖于该对象的状态

## 参与者

- **Context**：定义客户感兴趣的接口，维护一个 ConcreteState 子类的实例
- **State**：定义一个接口以封装与 Context 的一个特定状态相关的行为
- **ConcreteState**：每一子类实现一个与 Context 的一个状态相关的行为

## 代码示例

**状态接口：**

```java
public interface Weather {
    String getWeather();
    void doAction(Context context);
}
```

**上下文：**

```java
public class Context {
    private Weather weather;

    public String weatherMessage() {
        return weather.getWeather();
    }

    public Weather getWeather() {
        return weather;
    }

    public void setWeather(Weather weather) {
        this.weather = weather;
    }
}
```

**具体状态：**

```java
public class Rain implements Weather {
    @Override
    public String getWeather() {
        return "rain";
    }

    @Override
    public void doAction(Context context) {
        context.setWeather(this);
    }
}

public class Sunshine implements Weather {
    @Override
    public String getWeather() {
        return "Sunshine";
    }

    @Override
    public void doAction(Context context) {
        context.setWeather(this);
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        Context context = new Context();
        Weather rain = new Rain();
        rain.doAction(context);
        System.out.println(context.weatherMessage());

        context.setWeather(new Sunshine());
        System.out.println(context.weatherMessage());
    }
}
```

## 状态模式 vs 策略模式

| 模式 | 关注点 | 状态切换 |
|------|--------|----------|
| [[State_Pattern]] | 对象行为随状态改变 | 状态自动切换 |
| [[Strategy_Pattern]] | 算法族的封装 | 外部手动切换 |

## 应用场景

- 订单状态管理
- 游戏角色状态
- 工作流引擎
- TCP 连接状态
- 购物车状态

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Strategy_Pattern]] — 策略模式
- [[Observer_Pattern]] — 观察者模式
- [[Memento_Pattern]] — 备忘录模式
- [[raw/09-archive/设计模式/状态模式]] — 原始素材
