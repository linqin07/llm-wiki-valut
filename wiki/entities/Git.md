---
title: "Git"
type: entity
tags: [版本控制, 开源工具]
sources: [raw/01-articles/Java学习/git的使用/git命令.md, raw/01-articles/Java学习/git的使用/git标签操作.md, raw/01-articles/Java学习/git的使用/idea操作git.md]
last_updated: 2026-05-02
---

## 定义
Git 是分布式版本控制系统，是目前最流行的源代码管理工具。

## 常用命令
- **暂存**：git add .（新增+修改）、git add -u .（修改+删除）、git add -A .（全部）
- **远程仓库**：git remote -v 查看、git remote add origin \<url\> 关联
- **还原**：git reset --hard（撤销所有未提交）、git reset --soft HEAD~1（撤销 commit 保留代码）
- **标签**：git tag -a v1.0.1 \<commitid\> -m '说明'、git push --tag
- **忽略文件**：git update-index --assume-unchanged 暂时忽略
- **免登**：git config --global credential.helper store

## IDEA 中的高级操作
- **Stash**：备份当前修改，还原到 pull 状态
- **Reset HEAD**：--mixed（默认）、--soft（保留 add）、--hard（全部撤销）
- **Shelve Changes**：IDEA 特有，存储在 .idea/shelve 目录
- **交互式变基**：合并多个本地 commit，保持远程日志整洁

## 关联连接
- [[GitLab]] — 自托管 Git 服务
- [[IntelliJ_IDEA]] — IDE 集成
- [[摘要-git-使用]] — 来源
