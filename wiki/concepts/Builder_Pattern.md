---
title: "建造者模式（Builder Pattern）"
type: concept
tags: [设计模式, 创建型模式, Java]
sources:
  - raw/01-articles/设计模式/4.建造者模式/
last_updated: 2026-05-01
---

## 定义

建造者模式（Builder Pattern）是一种创建型设计模式，将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示。

**意图**：将一个复杂的对象构建和它的表示分离，使得同样的构建过程可以创建不同表示。

**主要解决**：对象创建过程复杂，需要多种表示。

**何时使用**：当创建复杂对象的算法应该独立于该对象的组成部分以及它们的装配方式时。

**关键代码**：构建内部静态类 Builder，属性和外部的类一致。

## 经典案例

> 小明想组装一个台式电脑，小明对电脑配置一窍不通，就直接跑到电脑城给装机老板说我要一台打游戏非常爽的电脑，麻烦你给装一下「配置什么的你给我推荐一下吧」，于是老板就让它的员工「小美」按小明的要求装了一个性能灰常牛 B 的电脑，1 个小时后电脑装好了，小明交钱拿电脑走人。不一会儿小张又来了，要一个满足平时写文章就可以的电脑，老板针对小张的要求给不同的装机配置。不同的人有不同的配置方案「但是装机流程是一样的」，这就是一个典型的建造者模式

## 实现步骤

1. 构建内部静态类 `Builder`，属性和外部的类一致
2. 为其添加 `setter` 方法，返回类型为 `Builder`
3. 构建 `build()` 方法，对外提供构建方法

## 代码示例

```java
public class Computer {
    private String cpu;
    private String hardDisk;
    private String mainBoard;
    private String memory;

    public Computer() {
    }

    public Computer(Builder builder) {
        this.cpu = builder.cpu;
        this.hardDisk = builder.hardDisk;
        this.mainBoard = builder.mainBoard;
        this.memory = builder.memory;
    }

    public static class Builder {
        private String cpu;
        private String hardDisk;
        private String mainBoard;
        private String memory;

        public Builder setCpu(String cpu) {
            this.cpu = cpu;
            return this;
        }

        public Builder setHardDisk(String hardDisk) {
            this.hardDisk = hardDisk;
            return this;
        }

        public Builder setMainBoard(String mainBoard) {
            this.mainBoard = mainBoard;
            return this;
        }

        public Builder setMemory(String memory) {
            this.memory = memory;
            return this;
        }

        public Computer build() {
            return new Computer(this);
        }
    }
}
```

## 应用场景

- 创建复杂对象（如电脑、汽车）
- 对象有多个可选参数
- 需要创建不同表示的对象
- StringBuilder、SQL 的 PreparedStatement

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Factory_Pattern]] — 工厂模式
- [[Abstract_Factory_Pattern]] — 抽象工厂模式
- [[Prototype_Pattern]] — 原型模式
