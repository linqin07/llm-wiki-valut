---
title: "代理模式（Proxy Pattern）"
type: concept
tags: [设计模式, 结构型模式, Java, AOP, 动态代理]
sources:
  - "[[摘要-design-patterns-java]]"
actionLink: "[[raw/09-archive/设计模式/代理模式]]"
last_updated: 2026-05-01
---

## 定义

代理模式（Proxy Pattern）是一种结构型设计模式，为其他对象提供一种代理以控制对这个对象的访问。

**意图**：为其他对象提供代理以控制访问。

**主要解决**：需要控制对对象的访问。

**何时使用**：想在访问一个类时做一些控制。

## 代理模式的类型

### 1. 静态代理

代理角色和真实角色实现同一个接口，具备统一的行为。在代理角色中，内置了真实角色，所有对真实角色方法的调用，都可以委托给代理角色。

**接口：**

```java
public interface UserInfo {
    public void queryUser();
    public void updateUser();
}
```

**实现类：**

```java
public class UserImpl implements UserInfo {
    @Override
    public void queryUser() {
        System.out.println("查询用户");
    }

    @Override
    public void updateUser() {
        System.out.println("更新用户");
    }
}
```

**代理类：**

```java
public class UserProxy implements UserInfo {
    private UserInfo userImpl;

    public UserProxy(UserInfo userImpl) {
        this.userImpl = userImpl;
    }

    @Override
    public void queryUser() {
        System.out.println("代理queryUser");
        userImpl.queryUser();
    }

    @Override
    public void updateUser() {
        System.out.println("代理updateUser");
        userImpl.updateUser();
    }
}
```

### 2. JDK 动态代理

基于接口的动态代理，使用 `InvocationHandler` 实现。

**代理处理器：**

```java
public class UserHandler implements InvocationHandler {
    private UserInfo userImpl;

    public UserHandler(UserInfo userImpl) {
        this.userImpl = userImpl;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        Object object = null;
        System.out.println("动态代理执行方法前");
        if ("queryUser".equals(method.getName())) {
            object = method.invoke(userImpl, args);
        }
        System.out.println("动态代理执行后");
        return object;
    }
}
```

**使用：**

```java
UserImpl user = new UserImpl();
UserHandler userHandler = new UserHandler(user);
UserInfo userProxy = (UserInfo) Proxy.newProxyInstance(
    ClassLoader.getSystemClassLoader(),
    new Class[]{UserInfo.class},
    userHandler
);
userProxy.queryUser();
```

**特性：**
- 不会代理嵌套的实现类，仅仅是代码复制
- Spring 的事务传播等特性无法进行代理
- 必须实现接口

### 3. CGLIB 动态代理

基于继承的动态代理，不需要接口。

**代理类：**

```java
public class UserCglibProxy implements MethodInterceptor {
    private Object target;

    public Object getInstance(Object target) {
        this.target = target;
        Enhancer enhancer = new Enhancer();
        enhancer.setSuperclass(this.target.getClass());
        enhancer.setCallback(this);
        return enhancer.create();
    }

    public Object intercept(Object object, Method method, Object[] args, MethodProxy methodProxy) throws Throwable {
        System.out.println("aop前");
        methodProxy.invokeSuper(object, args);
        System.out.println("aop后");
        return null;
    }
}
```

**特性：**
- 不用接口实现类
- 类不能是 final
- 可以嵌套代理（但 Spring 的 CGLIB 代理不会嵌套代理）

## 代理模式对比

| 类型 | 基于 | 优点 | 缺点 |
|------|------|------|------|
| 静态代理 | 接口 | 简单直观 | 需要重复编写代理方法 |
| JDK 动态代理 | 接口 | 代码量少，灵活 | 不能代理嵌套调用 |
| CGLIB 动态代理 | 继承 | 不需要接口，可嵌套代理 | 类不能是 final |

## 应用场景

- AOP（面向切面编程）
- 远程代理
- 虚拟代理
- 安全代理
- 日志记录
- 事务管理

## 关联连接

- [[Design_Patterns]] — 设计模式总览
- [[摘要-design-patterns-java]] — 来源摘要
- [[Adapter_Pattern]] — 适配器模式
- [[Decorator_Pattern]] — 装饰者模式
- [[Facade_Pattern]] — 外观模式
- [[raw/09-archive/设计模式/代理模式]] — 原始素材
