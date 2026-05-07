---
title: "OkHttp3"
type: entity
tags: [HTTP客户端, Java, Square, 开源]
sources:
  - "[[摘要-java-工具类]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Java学习/常用工具类/OkHttpUtil]]"
last_updated: 2026-05-02
---

## 定义
OkHttp3 是 Square 开发的高效 HTTP 客户端，支持 HTTP/2、连接池、GZIP 压缩等特性。

## 工具类封装要点
- 使用双重检查锁单例管理 OkHttpClient
- 支持 GET/POST 请求，最多重试 3 次
- 连接池配置：maxIdleConnections=200
- 线程池根据 CPU 核心数动态配置
- 支持 SSL 证书免验证（TrustAllCerts）
- 支持异步文件上传（MultipartBody）和下载

## 关联连接
- [[摘要-java-工具类]] — 来源摘要
- [[摘要-java-工具类]] — Java 工具类汇总
- [[raw/09-archive/设计模式/raw/09-archive/Java学习/常用工具类/OkHttpUtil]] — 原始素材
