---
title: "CC捕获: 有用到了obsidian cli工具了吗"
type: source
tags:
  - 来源
  - CC捕获
  - E--llm-wiki-vault
sources:
  - ~/.claude/projects/E--llm-wiki-vault
last_updated: 2026-05-01
---

## 来源
- **项目**: E--llm-wiki-vault
- **日期**: 2026-05-01
- **对话条目**: 43 条

## 问题与解决

### 问题
> 有用到了obsidian cli工具了吗

### 解决过程
没有。我检查了 `obsidian-cli` 是否可用：

```bash
which obsidian-cli  # 返回 NOT_FOUND
```

由于 `obsidian-cli` 未安装，我回退使用了 Write 工具创建所有页面。这是符合 CLAUDE.md 规定的回退策略：

> **工具优先级**：默认使用 CLI 工具执行 vault 操作，仅当 CLI 工具不可用或操作失败时，回退到 Claude Code 内置工具。

如果你需要安装 obsidian-cli，可以告诉我，我可以帮你配置。

---

### 问题
> 检测obsidian相关skill能否使用

### 解决过程
让我测试几个 obsidian 相关的 skill。

Skill 已加载，让我尝试使用 obsidian CLI 读取文件。

**测试结果：obsidian-cli 不可用**

`obsidian` CLI 工具未安装或未添加到 PATH。根据 skill 文档，它需要：
1. 安装 Obsidian CLI（参考 https://help.obsidian.md/cli）
2. Obsidian 应用处于打开状态

**替代方案：** 我继续使用 Read/Write/Edit 等内置工具操作 vault 文件，功能完全相同，只是 token 消耗略高。

需要我帮你安装 obsidian CLI 吗？

---

### 问题
> 为什么我无法使用这个命令，但是外部的cmd可以

### 解决过程
这是因为 Claude Code 使用 **bash** shell，而你的 `obsidian` 命令在 **Windows cmd** 的 PATH 中。两者的 PATH 环境变量不同。

让我排查一下：

**问题确认：** Obsidian 已安装，但 CLI 功能可能未启用。

**解决方案：**

1. **打开 Obsidian** → 设置 → 第三方插件 → 启用「Obsidian CLI」
2. 或者检查 Obsidian 版本是否 ≥ 1.5.8（CLI 需要此版本）

如果 CLI 已启用，它通常位于：
```
C:\Users\86147\AppData\Local\Programs\obsidian\obsidian-cli.exe
```

你可以尝试在 cmd 中运行 `obsidian --version` 确认是否可用。如果 cmd 中可用但我这里不行，可以告诉我完整路径，我直接调用。

---

### 问题
> 我找不到这个，但是我cmd确实可以打开。86147@linqin MINGW64 /e
$ obsidian

Obsidian CLI

Usage: obsidian <command> [options]

### 解决过程
明白了，你用的是 **Git Bash (MINGW64)**，而 Claude Code 用的是另一个 bash 环境。让我检查一下：

No response requested.

---

### 问题
> 现在我用cmd启动的claude，再检测一下

### 解决过程
现在 obsidian CLI 可用了！让我测试读取功能：

**obsidian CLI 现在可用！** 让我再测试搜索功能：

**检测结果：obsidian CLI 已可用！**

| 命令 | 状态 |
|------|------|
| `obsidian read` | ✓ 正常 |
| `obsidian search` | ✓ 正常 |
| `obsidian create` | ✓ 可用 |
| `obsidian append` | ✓ 可用 |

**问题原因：** 之前你用 Git Bash (MINGW64) 启动 Claude Code，而 `obsidian` 命令在 Windows cmd 的 PATH 中。现在用 cmd 启动，PATH 一致，CLI 就可用了。

后续 ingest、query、lint 等操作我会优先使用 `obsidian` CLI 工具，节省 token 消耗。

---

### 问题
> 我是用tabby工具的git bash打开的。再里面cmd和git bash都不行，为啥

### 解决过程
No response requested.

---

### 问题
> 我是用tabby工具的git bash打开的。再里面cmd和git bash都不行，为啥

### 解决过程
这很有趣。让我帮你排查一下原因：

**找到原因了！**

`obsidian` CLI 安装在：
```
/d/Program Files/Obsidian/obsidian  (版本 1.12.4)
```

**问题根源：**

| 环境 | PATH 包含 `D:\Program Files\Obsidian` | 结果 |
|------|--------------------------------------|------|
| Claude Code (cmd 启动) | ✓ 有 | 可用 |
| Tabby Git Bash | ✗ 没有 | 不可用 |

**Tabby Git Bash 不行的原因：**
Tabby 的 Git Bash 继承的 PATH 环境变量可能没有包含 `D:\Program Files\Obsidian` 这个路径。Git Bash 的 PATH 通常来自 `/etc/profile` 或 `~/.bashrc`，而不是 Windows 系统 PATH。

**解决方案：**

在 Tabby Git Bash 中手动添加路径：
```bash
export PATH="$PATH:/d/Program Files/Obsidian"
```

或者永久生效，添加到 `~/.bashrc`：
```bash
echo 'export PATH="$PATH:/d/Program Files/Obsidian"' >> ~/.bashrc
```

---

### 问题
> 我发现只有临时的生效，永久的不行。是不是tabby的问题，外面的git bash是可以的

### 解决过程
是的，很可能是 Tabby 的问题。让我帮你排查：

**问题确认：** 你已经在 `~/.bashrc` 中添加了配置，但 Tabby 没有读取它。

**原因：** Tabby 启动 Git Bash 时使用的是 **login shell**，它只读取 `~/.bash_profile`，不读取 `~/.bashrc`。

**解决方案：** 把 PATH 配置添加到 `~/.bash_profile`：

看到了，`~/.bash_profile` 只有 conda 配置。有两个解决方案：

**方案 1：** 直接在 `~/.bash_profile` 添加 PATH（推荐）
```bash
echo 'export PATH="$PATH:/d/Program Files/Obsidian"' >> ~/.bash_profile
```

**方案 2：** 让 `~/.bash_profile` 加载 `~/.bashrc`
```bash
echo 'source ~/.bashrc' >> ~/.bash_profile
```

方案 2 更通用，以后在 `~/.bashrc` 添加的配置都会被 Tabby 读取。

你选哪个？我帮你执行。

---

### 问题
> 方案二

### 解决过程
完成。现在重启 Tabby 终端，新的 Git Bash 会话就会加载 `~/.bashrc`，`obsidian` 命令就能用了。

---

### 问题
> 但是tabby的cmd还不行

### 解决过程
cmd 不读取 `~/.bashrc`，它使用 Windows 系统 PATH。让我检查一下：

Windows PATH 中已经有 `D:\Program Files\Obsidian` 了。让我测试一下：

在我这里 cmd 可以运行 `obsidian`。如果 Tabby 的 cmd 不行，可能是：

**原因：** Tabby 启动 cmd 时可能没有继承完整的 Windows 系统 PATH，或者 Tabby 有自己的环境变量配置覆盖了 PATH。

**解决方案：**

1. **重启 Tabby** — 如果你刚添加了 PATH，需要重启 Tabby 才能生效
2. **检查 Tabby 设置** — Tabby 可能有"继承系统环境变量"的选项
3. **在 Tabby cmd 中手动测试** — 打开 Tabby 的 cmd，输入：
   ```
   echo %PATH%
   ```
   看看是否包含 `D:\Program Files\Obsidian`

你能帮我看看 Tabby cmd 中的 `%PATH%` 输出吗？

## 关联连接
- [[index]] — 知识库总目录