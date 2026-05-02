---
title: "Feign"
type: entity
tags: [Spring-Cloud, HTTP客户端, 声明式调用, RPC]
sources: [raw/01-articles/SpringCloud/6.feign.md]
last_updated: 2026-05-01
---

## 定义

Feign 是 Netflix 开源的声明式 HTTP 客户端，Spring Cloud 对其进行了增强集成。通过接口和注解的方式定义 HTTP 调用，简化微服务间的远程调用。

## 关键信息

### 发送表单请求
```java
@RequestMapping(value="/someThing/someMethod",
                method=RequestMethod.POST,
                consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE)
ApiResponse someThing(@RequestBody String formParam);
```

调用时需手动封装参数为 URL 编码格式：
```java
List<NameValuePair> nvps = new ArrayList<>();
nvps.add(new BasicNameValuePair("key1", key1.toString()));
nvps.add(new BasicNameValuePair("key2", StringUtils.join(key2, ",")));
String queryStr = URLEncodedUtils.format(nvps, Consts.UTF_8);
someThing(queryStr);
```

### Maven 多模块公共接口设计
- **login-common**：存放 Feign 接口，提供给其他微服务调用
- **login-server**：存放业务代码，Controller 实现 common 中的 Feign 接口

这种设计实现了接口定义与实现的分离，其他微服务只需依赖 common 模块即可调用。

## 关联连接
- [[摘要-spring-cloud-微服务]] — 来源
- [[Spring_Cloud_Gateway]] — 网关路由到 Feign 服务
- [[Spring_Boot]] — 基础框架
