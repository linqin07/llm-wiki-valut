---
title: "GitLab"
type: entity
tags: [Git, DevOps, 自托管, 开源]
sources: [raw/01-articles/Java学习/git的使用/安装gitlab/CentOS7安装维护Gitlab.md]
last_updated: 2026-05-02
---

## 定义
GitLab 是基于 Git 的自托管 DevOps 平台，提供代码仓库管理、CI/CD、问题跟踪等功能。

## 安装方式
- 官方 yum 安装
- 清华镜像源安装
- Docker 安装

## 运维管理
- **配置文件**：/etc/gitlab/gitlab.rb，设置 external_url
- **服务管理**：gitlab-ctl start/stop/restart/status/reconfigure
- **备份**：gitlab-rake gitlab:backup:create，自动备份用 crontab
- **恢复**：先停止 unicorn 和 sidekiq，再 gitlab-rake gitlab:backup:restore
- **重置密码**：gitlab-rails console production 进入控制台

## 内存优化
调整 postgresql shared_buffers、unicorn worker_processes

## 关联连接
- [[Git]] — 底层版本控制
- [[Docker]] — Docker 安装方式
- [[Nginx]] — 反向代理配置
- [[摘要-gitlab-安装维护]] — 来源
