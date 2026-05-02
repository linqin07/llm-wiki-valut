---
title: "Nginx"
type: entity
tags: [Web服务器, 反向代理, 负载均衡, 开源]
sources: [raw/01-articles/Linux/Nginx/1.安装.md, raw/01-articles/Linux/Nginx/2.配置.md]
last_updated: 2026-05-02
---

## 定义
Nginx 是高性能的 HTTP 和反向代理服务器，也用作负载均衡器和邮件代理。

## 安装
- 源码编译：依赖 gcc、pcre-devel、zlib、openssl
- yum 安装：配置 nginx.repo 或 EPEL 源

## 配置要点
- location 匹配优先级：= > ^~ > 正则 > 普通前缀 > /
- upstream 支持 weight、max_fails、fail_timeout、down、backup
- proxy_pass 末尾有 / 去掉匹配路径段，无 / 拼接完整路径
- root 拼接 location 路径，alias 替换 location 路径
- worker_processes 设为 CPU 核心数

## 关联连接
- [[Docker]] — 容器中部署
- [[摘要-nginx-配置]] — 来源
