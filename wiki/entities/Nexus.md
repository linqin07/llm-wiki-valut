---
title: "Nexus"
type: entity
tags: [私服, Maven, 制品仓库, Sonatype]
sources:
  - "[[摘要-构建工具]]"
actionLink: "[[raw/09-archive/设计模式/raw/09-archive/Java学习/构建工具/Maven]]"
last_updated: 2026-05-02
---

## 定义
Nexus 是 Sonatype 开发的制品仓库管理器，用于托管 Maven 私服和其他软件包。

## 仓库类型
- **Release 仓库**：只能上传一次，不可覆盖
- **SNAPSHOT 仓库**：JAR 名称必须包含 SNAPSHOT

## 关联连接
- [[Maven]] — 构建工具集成
- [[摘要-构建工具]] — 来源摘要
- [[raw/09-archive/设计模式/raw/09-archive/Java学习/构建工具/Maven]] — 原始素材
