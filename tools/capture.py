#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
capture.py — 从 Claude Code 对话中提取有价值的知识，生成干净文章
用法:
  python tools/capture.py                          # 交互式
  python tools/capture.py --list                   # 列出所有项目
  python tools/capture.py <project>                # 指定项目
  python tools/capture.py <project> <session-id>   # 指定对话
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Windows 控制台 UTF-8 支持
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        os.system("chcp 65001 >nul 2>&1")

CLAUDE_DIR = Path.home() / ".claude" / "projects"
SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = VAULT_DIR / "raw" / "01-articles"


def get_projects():
    """列出所有有对话的项目"""
    projects = []
    if not CLAUDE_DIR.exists():
        return projects
    for d in sorted(CLAUDE_DIR.iterdir()):
        if d.is_dir():
            jsonl_files = list(d.glob("*.jsonl"))
            if jsonl_files:
                projects.append((d.name, len(jsonl_files), d))
    return projects


def get_sessions(project_dir):
    """列出项目中的对话"""
    sessions = []
    for f in sorted(project_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True):
        lines = f.read_text(encoding="utf-8", errors="ignore").count("\n")
        size = f.stat().st_size
        # 提取第一条用户消息作为预览
        preview = extract_first_user_message(f)
        sessions.append((f.stem, lines, size, preview, f))
    return sessions


def extract_first_user_message(jsonl_path):
    """提取对话中第一条用户消息作为预览"""
    try:
        with open(jsonl_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if obj.get("type") == "user":
                    msg = obj.get("message", {})
                    content = msg.get("content", "")
                    if isinstance(content, str) and not content.startswith("<"):
                        return content[:80].replace("\n", " ")
        return "(无用户消息)"
    except Exception:
        return "(无法解析)"


def extract_conversation(jsonl_path, project_name):
    """解析 JSONL，提取有价值的对话内容"""
    turns = []

    with open(jsonl_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            obj_type = obj.get("type", "")
            timestamp = obj.get("timestamp", "")

            if obj_type == "user":
                msg = obj.get("message", {})
                content = msg.get("content", "")
                if isinstance(content, str):
                    # 跳过所有 XML 标签开头的系统消息
                    if content.lstrip().startswith("<"):
                        continue
                    # 跳过 session continuation 摘要
                    if content.startswith("This session is being continued"):
                        continue
                    if content.strip():
                        turns.append(("user", content.strip(), timestamp))

            elif obj_type == "assistant":
                msg = obj.get("message", {})
                content = msg.get("content", "")
                if isinstance(content, list):
                    text_parts = []
                    for block in content:
                        if block.get("type") == "text" and block.get("text", "").strip():
                            text_parts.append(block["text"].strip())
                    if text_parts:
                        combined = "\n\n".join(text_parts)
                        # 清理 thinking 标签
                        combined = re.sub(r"<thinking>.*?</thinking>", "", combined, flags=re.DOTALL).strip()
                        if combined:
                            turns.append(("assistant", combined, timestamp))

    if not turns:
        return None

    # 提取主题
    topic = "未知主题"
    for role, text, _ in turns:
        if role == "user":
            topic = text[:50].replace("\n", " ").strip()
            break

    # 提取日期
    date_str = datetime.now().strftime("%Y-%m-%d")
    for _, _, ts in turns:
        if ts:
            try:
                date_str = ts[:10]
            except Exception:
                pass
            break

    # 生成 Markdown
    lines = []
    lines.append("---")
    lines.append(f'title: "CC捕获: {topic}"')
    lines.append("type: source")
    lines.append(f"tags: [来源, CC捕获, {project_name}]")
    lines.append(f"sources: [~/.claude/projects/{project_name}]")
    lines.append(f"last_updated: {date_str}")
    lines.append("---")
    lines.append("")
    lines.append("## 来源")
    lines.append(f"- **项目**: {project_name}")
    lines.append(f"- **日期**: {date_str}")
    lines.append(f"- **对话条目**: {len(turns)} 条")
    lines.append("")
    lines.append("## 问题与解决")
    lines.append("")

    # 合并连续的 assistant 消息，配对 user→assistant
    current_question = None
    current_solutions = []

    for role, text, _ in turns:
        if role == "user":
            # 输出上一对
            if current_question is not None and current_solutions:
                lines.append(f"### 问题")
                lines.append(f"> {current_question[:300]}")
                lines.append("")
                lines.append("### 解决过程")
                combined = "\n\n".join(current_solutions)
                if len(combined) > 2000:
                    combined = combined[:2000] + "\n\n... (已截断)"
                lines.append(combined)
                lines.append("")
                lines.append("---")
                lines.append("")
            current_question = text
            current_solutions = []
        elif role == "assistant":
            current_solutions.append(text)

    # 输出最后一对
    if current_question and current_solutions:
        lines.append(f"### 问题")
        lines.append(f"> {current_question[:300]}")
        lines.append("")
        lines.append("### 解决过程")
        combined = "\n\n".join(current_solutions)
        if len(combined) > 2000:
            combined = combined[:2000] + "\n\n... (已截断)"
        lines.append(combined)
        lines.append("")

    lines.append("## 关联连接")
    lines.append(f"- [[index]] — 知识库总目录")

    return "\n".join(lines), topic, date_str


def main():
    args = sys.argv[1:]

    # --list
    if args and args[0] in ("--list", "-l"):
        projects = get_projects()
        print("可用项目:")
        for i, (name, count, _) in enumerate(projects, 1):
            print(f"  {i}) {name} ({count} 个对话)")
        return

    # 确定项目
    project_name = None
    session_id = None

    if args:
        project_name = args[0]
    if len(args) > 1:
        session_id = args[1]

    projects = get_projects()

    if not project_name:
        # 交互式选择
        print("可用项目:")
        for i, (name, count, _) in enumerate(projects, 1):
            print(f"  {i}) {name} ({count} 个对话)")
        print()
        choice = input("选择项目编号或输入项目名: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(projects):
                project_name = projects[idx][0]
        else:
            project_name = choice

    if not project_name:
        print("错误: 未选择项目", file=sys.stderr)
        sys.exit(1)

    # 查找项目目录
    project_dir = CLAUDE_DIR / project_name
    if not project_dir.exists():
        # 模糊匹配
        matches = [d for d in CLAUDE_DIR.iterdir() if project_name in d.name]
        if matches:
            project_dir = matches[0]
            project_name = project_dir.name
            print(f"匹配到项目: {project_name}")
        else:
            print(f"错误: 项目不存在: {project_name}", file=sys.stderr)
            sys.exit(1)

    # 选择对话
    sessions = get_sessions(project_dir)

    if not session_id:
        print(f"\n项目 {project_name} 的对话:")
        for i, (sid, lines, size, preview, _) in enumerate(sessions, 1):
            print(f"  {i}) {sid} [{lines}行, {size//1024}KB] {preview}")
        print()
        choice = input("选择对话编号 (默认=最新): ").strip()
        if not choice:
            session_id = sessions[0][0] if sessions else None
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(sessions):
                session_id = sessions[idx][0]
        else:
            session_id = choice

    # 查找对话文件
    jsonl_path = project_dir / f"{session_id}.jsonl"
    if not jsonl_path.exists():
        print(f"错误: 对话文件不存在: {jsonl_path}", file=sys.stderr)
        sys.exit(1)

    print(f"正在提取对话 {session_id}...")

    result = extract_conversation(jsonl_path, project_name)
    if result is None:
        print("错误: 对话中没有提取到有效内容", file=sys.stderr)
        sys.exit(1)

    content, topic, date_str = result

    # 生成文件名（限制总长度）
    slug = re.sub(r"[^\w一-鿿]+", "-", topic)[:20].strip("-").lower()
    filename = f"cc-捕获-{date_str}-{slug}.md"
    filename = re.sub(r"[^a-zA-Z0-9一-鿿._-]", "-", filename)
    filename = re.sub(r"-+", "-", filename)

    output_path = OUTPUT_DIR / filename
    output_path.write_text(content, encoding="utf-8")

    print(f"已生成: {output_path}")
    print(f"下一步: 在 wiki 项目中运行 /ingest 完成入库")


if __name__ == "__main__":
    main()
