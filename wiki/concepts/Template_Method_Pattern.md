---
title: "模板方法模式（Template Method Pattern）"
type: concept
tags: [设计模式, 行为型模式, Java, 继承, 代码复用]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/模板方法模式]]"
last_updated: 2026-05-01
---

## 定义

模板方法模式（Template Method Pattern）是一种行为型设计模式，定义一个操作中的算法的骨架，而将一些步骤延迟到子类中。Template Method 使得子类可以不改变一个算法的结构即可重定义该算法的某些特定步骤。

**意图**：定义算法骨架，延迟某些步骤。

**主要解决**：算法结构固定，某些步骤可变。

**核心思想**：继承是复用代码的重要方式。

## 代码示例

构建一个创建规则文件的类，创建规则文件有一部分配置是公共的，其余的配置是不同的。

**抽象类：**

```java
public abstract class AbstractAlertRuleCreator implements AlertRuleInterface {
    @Override
    public String create() {
        // 公有部分
        String common = createCommonConfig();
        // 私有部分
        String ziji = createConfig();
        return common + ziji;
    }

    /**
     * 私有部分
     */
    protected abstract String createConfig();

    /**
     * 公有部分
     */
    private String createCommonConfig() {
        return "公共 ";
    }
}
```

**子类实现：**

```java
public class Config1 extends AbstractAlertRuleCreator {
    @Override
    protected String createConfig() {
        return "config1";
    }
}

public class Config2 extends AbstractAlertRuleCreator {
    @Override
    protected String createConfig() {
        return "config2";
    }
}
```

**测试：**

```java
Config1 config1 = new Config1();
System.err.println(config1.create());

Config2 config2 = new Config2();
System.err.println(config2.create());
```

**输出：**

```
公共 config1
公共 config2
```

## 模板方法的结构

1. **抽象类（AbstractClass）**：定义模板方法和抽象步骤
2. **具体类（ConcreteClass）**：实现抽象步骤

## 应用场景

- 数据库访问层（连接、查询、关闭的骨架固定）
- servlet 的 doGet/doPost
- JUnit 的 setUp/tearDown
- Spring 的 JdbcTemplate
- 工作流引擎

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Strategy_Pattern]] — 策略模式
- [[Factory_Pattern]] — 工厂模式
- [[raw/09-archive/设计模式/模板模式]] — 原始素材
