---
title: "组合模式（Composite Pattern）"
type: concept
tags: [设计模式, 结构型模式, Java, 树形结构]
sources:
  - raw/01-articles/设计模式/11.组合模式/
last_updated: 2026-05-01
---

## 定义

组合模式（Composite Pattern）是一种结构型设计模式，将对象组合成树形结构以表示"部分-整体"的层次结构。Composite 使得用户对单个对象和组合对象的使用具有一致性。

**意图**：表示对象的部分-整体层次结构。

**主要解决**：表示对象的部分-整体层次结构。

**何时使用**：
- 表示对象的部分-整体层次结构
- 希望用户忽略组合对象与单个对象的不同，用户将统一地使用组合结构中的所有对象

## 参与者

- **Component**：为组合中的对象声明接口，实现所有类共有接口的缺省行为
- **Leaf**：在组合中表示叶节点对象，叶节点没有子节点
- **Composite**：定义有子部件的那些部件的行为，存储子部件
- **Client**：通过 Component 接口操纵组合部件的对象

## 代码示例

**抽象类（Component）：**

```java
public abstract class Employer {
    public List<Employer> employers;
    private String name;

    public abstract void add(Employer employer);
    public abstract void delete(Employer employer);

    public Employer() {
        System.out.println("初始化Employer");
        employers = new ArrayList<>();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

**叶子节点（Leaf）：**

```java
public class Programmer extends Employer {
    public Programmer(String name) {
        super.setName(name);
        employers = null;
    }

    @Override
    public void add(Employer employer) {}

    @Override
    public void delete(Employer employer) {}
}

public class ProjectAssistant extends Employer {
    public ProjectAssistant(String name) {
        setName(name);
        employers = null;
    }

    @Override
    public void add(Employer employer) {}

    @Override
    public void delete(Employer employer) {}
}
```

**组合节点（Composite）：**

```java
public class ProjectManager extends Employer {
    public ProjectManager(String name) {
        setName(name);
    }

    @Override
    public void add(Employer employer) {
        employers.add(employer);
    }

    @Override
    public void delete(Employer employer) {
        employers.remove(employer);
    }
}
```

**测试：**

```java
public class Test {
    public static void main(String[] args) {
        ProjectManager pm = new ProjectManager("项目经理");
        ProjectAssistant pa = new ProjectAssistant("项目助理");
        Programmer no1 = new Programmer("程序员1号");
        Programmer no2 = new Programmer("程序员2号");

        pm.add(pa);
        pm.add(no1);
        pm.add(no2);

        for (Employer employer : pm.employers) {
            System.out.println(employer.getName());
        }
    }
}
```

## 应用场景

- 文件系统（文件和文件夹）
- 组织架构（部门和员工）
- GUI 组件树
- 菜单系统
- XML/HTML DOM

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Iterator_Pattern]] — 迭代器模式
- [[Visitor_Pattern]] — 访问者模式
