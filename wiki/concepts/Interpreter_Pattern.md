---
title: "解释器模式（Interpreter Pattern）"
type: concept
tags: [设计模式, 行为型模式, Java, 语法解析]
sources:
  - raw/01-articles/设计模式/15.解析器模式/
last_updated: 2026-05-01
---

## 定义

解释器模式（Interpreter Pattern）是一种行为型设计模式，给定一个语言，定义它的文法的一种表示，并定义一个解释器，这个解释器使用该表示来解释语言中的句子。

**意图**：定义语言的文法表示。

**主要解决**：需要解释执行特定语言。

**何时使用**：当有一个语言需要解释执行，并且你可将该语言中的句子表示为一个抽象语法树时。

**最佳场景**：
- 该文法简单（对于复杂的文法，文法的类层次变得庞大而无法管理）
- 效率不是一个关键问题（最高效的解释器通常不是通过直接解释语法分析树实现的）

## 参与者

- **AbstractExpression（抽象表达式）**：声明一个抽象的解释操作
- **TerminalExpression（终结符表达式）**：实现与文法中的终结符相关联的解释操作
- **NonterminalExpression（非终结符表达式）**：为文法中的非终结符实现解释操作
- **Context（上下文）**：包含解释器之外的一些全局信息
- **Client（客户）**：构建表示该文法定义的语言中一个特定的句子的抽象语法树

## 代码示例

**抽象表达式：**

```java
public abstract class Expression {
    abstract void interpret(Context ctx);
}
```

**上下文：**

```java
public class Context {
    private String content;
    private List<Expression> list = new ArrayList<Expression>();

    public String getContent() {
        return this.content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public void add(Expression eps) {
        list.add(eps);
    }

    public List<Expression> getList() {
        return list;
    }
}
```

**具体表达式：**

```java
public class AdvanceExpression extends Expression {
    @Override
    void interpret(Context ctx) {
        System.out.println("这是高级解析器!");
    }
}

public class SimpleExpression extends Expression {
    @Override
    void interpret(Context ctx) {
        System.out.println("这是普通解析器!");
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        Context ctx = new Context();
        ctx.add(new SimpleExpression());
        ctx.add(new AdvanceExpression());

        for (Expression expression : ctx.getList()) {
            expression.interpret(ctx);
        }
    }
}
```

## 应用场景

- SQL 解析
- 正则表达式
- 数学表达式计算
- 编译器
- 配置文件解析

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Visitor_Pattern]] — 访问者模式
