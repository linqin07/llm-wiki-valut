---
title: "Docker"
type: entity
tags: [容器, DevOps, 开源]
sources: [raw/01-articles/Linux/docker/1.简介安装.md, raw/01-articles/Linux/docker/2.Docker用法.md]
last_updated: 2026-05-02
---

## 定义
Docker 是开源的容器化平台，通过 CS 架构（daemon + client）实现应用的打包、分发和运行。

## 核心概念
- **Image（镜像）**：只读模板
- **Container（容器）**：隔离运行环境，一个镜像可运行多个容器
- **Registry/Hub**：镜像仓库

## 常用操作
- daemon.json 配置：registry-mirrors（加速）、graph（存储目录）、live-restore
- Dockerfile 核心指令：FROM、RUN、COPY/ADD、EXPOSE、WORKDIR、VOLUME、CMD/ENTRYPOINT
- 数据卷容器通过 --volumes-from 实现多容器数据共享
- docker-compose 通过 YAML 文件定义多服务编排

## 关联连接
- [[Nexus]] — 私服搭建
- Kubernetes — 容器编排
- [[摘要-docker-使用]] — 来源
- [[摘要-linux-shell-脚本]] — Shell 脚本
- [[摘要-linux-系统运维]] — Linux 运维
