---
title: "Jenkins"
type: entity
tags: [CI/CD, 持续集成, DevOps, 开源]
sources: [raw/01-articles/Java学习/构建工具/Jenkins安装.md]
last_updated: 2026-05-02
---

## 定义
Jenkins 是开源的自动化服务器，用于实现 CI/CD（持续集成/持续部署）流水线。

## 安装方式
下载 jenkins.war 并通过 `java -jar jenkins.war --httpPort=8899` 启动。

## 配置要点
- 用户数据存储在 /root/.jenkins 目录
- 修改更新源为清华镜像（sed 替换 default.json 中的 URL）
- 工作空间路径在 config.xml 中修改 workspaceDir

## 离线部署
外网下载插件后复制 plugins 目录到内网机器，或直接复制整个 .jenkins 文件夹迁移。

## 关联连接
- [[Maven]] — 构建工具
- [[GitLab]] — 代码仓库集成
- [[摘要-jenkins-安装]] — 来源
