#!/usr/bin/env bash
# capture.sh — 从 Claude Code 对话中提取知识的便捷入口
# 实际逻辑在 capture.py 中
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python "$SCRIPT_DIR/capture.py" "$@"
