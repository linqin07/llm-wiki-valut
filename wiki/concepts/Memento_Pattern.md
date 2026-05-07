---
title: "备忘录模式（Memento Pattern）"
type: concept
tags: [设计模式, 行为型模式, Java, 状态保存, 撤销]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/备忘录模式]]"
last_updated: 2026-05-01
---

## 定义

备忘录模式（Memento Pattern）是一种行为型设计模式，在不破坏封装性的前提下，捕获一个对象的内部状态，并在该对象之外保存这个状态。这样以后就可将该对象恢复到原先保存的状态。

**意图**：在不破坏封装的前提下保存和恢复对象状态。

**主要解决**：需要保存和恢复对象的历史状态。

**何时使用**：
- 必须保存一个对象在某一个时刻的（部分）状态，这样以后需要时它才能恢复到先前的状态
- 如果用一个接口来让其它对象直接得到这些状态，将会暴露对象的实现细节并破坏对象的封装性

## 参与者

- **Memento（备忘录）**：存储原发器对象的内部状态
- **Originator（原发器）**：创建一个备忘录，用以记录当前时刻它的内部状态；使用备忘录恢复内部状态
- **Caretaker（看守人）**：负责保存好备忘录，不能对备忘录的内容进行操作或检查

## 代码示例

**备忘录：**

```java
public class Text {
    private String state;

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public Text(String state) {
        this.state = state;
    }
}
```

**原发器：**

```java
public class Man {
    private String state;

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public void setText(Text text) {
        state = text.getState();
    }

    public Text createText() {
        return new Text(state);
    }

    public void showText() {
        System.out.println(state);
    }
}
```

**看守人：**

```java
public class Caretaker {
    private Text text;

    public Text getText() {
        return text;
    }

    public void setText(Text text) {
        this.text = text;
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        Man man = new Man();
        man.setState("开会中");
        man.showText();

        Caretaker caretaker = new Caretaker();
        caretaker.setText(man.createText());

        // 状态修改
        man.setState("吃饭中");
        man.showText();

        // 设置备忘录中的状态
        man.setText(caretaker.getText());
        man.showText();
    }
}
```

## 应用场景

- 撤销/重做功能
- 游戏存档
- 数据库事务回滚
- 历史记录

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Command_Pattern]] — 命令模式
- [[State_Pattern]] — 状态模式
- [[raw/09-archive/设计模式/备忘录模式]] — 原始素材
