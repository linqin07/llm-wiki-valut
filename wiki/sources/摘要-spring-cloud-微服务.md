---
title: "摘要-spring-cloud-微服务"
type: source
tags: [Spring-Cloud, 微服务, Java, 来源]
sources:
  - "raw/09-archive/SpringCloud/"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/SpringCloud]]"
last_updated: 2026-05-01
---

## 核心摘要

本组资料涵盖了 Spring Cloud 微服务体系的核心组件实践笔记，包括服务注册中心（Eureka、Nacos）、服务网关（Spring Cloud Gateway、Zuul）和声明式 HTTP 客户端（Feign）。资料以实战配置为主，包含完整的依赖配置、启动类、路由规则、过滤器链等代码示例，并记录了开发过程中遇到的典型问题与解决方案（如 Zuul 文件上传超时、Gateway 请求体读取等）。

## 内容清单

| 文件 | 主题 |
|------|------|
| 1.Eureka服务注册中心.md | Eureka 注册中心搭建、CAP 原理、自定义负载均衡 |
| 2.SpringCloud-cli.md | Spring Boot CLI 安装与 Spring Cloud 服务快速启动 |
| 3.服务网关SpringCloudGateWay.md | Gateway 路由、过滤器、整合 Eureka、请求体处理 |
| 4.接入nacos.md | Spring Boot 接入 Nacos 配置中心和服务发现 |
| 5.zuul 网关.md | Zuul 网关文件上传超时问题与 /zuul 前缀绕过 |
| 6.feign.md | Feign 表单请求发送与多模块公共接口设计 |

## 关联连接
- [[Eureka]] — 服务注册中心实体
- [[Nacos]] — 阿里巴巴服务治理组件
- [[Spring_Cloud_Gateway]] — 新一代服务网关
- [[Zuul]] — Netflix 服务网关
- [[Feign]] — 声明式 HTTP 客户端
- [[服务注册中心]] — 核心概念
- [[服务网关]] — 核心概念
- [[CAP定理]] — 分布式系统理论基础
- [[raw/09-archive/设计模式/raw/09-archive/SpringCloud]] — 原始素材
