#!/usr/bin/env python3
"""
认知提取脚本 — 将存档时的认知收获推送到外部知识库。

用法:
    python scripts/cognitive-extract.py --backend <backend> --title "..." --body "..."
    python scripts/cognitive-extract.py --file <candidates.json>

后端（通过 --backend 或 COGNITIVE_EXTRACT_BACKEND 环境变量选择）:
    markdown      追加到 cognitive-log.md（默认，零外部依赖）
    obsidian-ntfy 通过 ntfy.sh 推送到 Obsidian（需 OBSIDIAN_NTFY_KEY）
    none          仅 stdout 打印，不发送

环境变量:
    COGNITIVE_EXTRACT_BACKEND   后端类型（默认: markdown）
    OBSIDIAN_NTFY_KEY           ntfy.sh 推送密钥（obsidian-ntfy 后端必需）
    NTFY_TOPIC                  ntfy.sh 主题（默认: cognitive-extract）

返回: exit code 0=成功, 1=部分失败, 2=输入错误
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_NTFY_TOPIC = "cognitive-extract"
DEFAULT_BACKEND = "markdown"
BACKENDS = ("markdown", "obsidian-ntfy", "none")


def log(msg: str) -> None:
    print(json.dumps({"level": "info", "message": msg}))


def error(msg: str) -> None:
    print(json.dumps({"level": "error", "message": msg}), file=sys.stderr)


def result(ok: bool, detail: str = "") -> None:
    print(json.dumps({"ok": ok, "detail": detail}))


def read_input(args: argparse.Namespace) -> list[dict]:
    if args.file:
        path = Path(args.file)
        if not path.exists():
            error(f"输入文件不存在: {args.file}")
            sys.exit(2)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return [data]
    if args.title and args.body:
        return [{"title": args.title, "body": args.body}]
    error("请提供 --title + --body 或 --file")
    sys.exit(2)


def get_backend(args: argparse.Namespace) -> str:
    backend = args.backend or os.environ.get("COGNITIVE_EXTRACT_BACKEND", DEFAULT_BACKEND)
    if backend not in BACKENDS:
        error(f"不支持的后端: {backend}，可选: {', '.join(BACKENDS)}")
        sys.exit(2)
    return backend


def send_obsidian_ntfy(entries: list[dict]) -> bool:
    key = os.environ.get("OBSIDIAN_NTFY_KEY")
    if not key:
        error("obsidian-ntfy 后端需要 OBSIDIAN_NTFY_KEY 环境变量")
        return False
    topic = os.environ.get("NTFY_TOPIC", DEFAULT_NTFY_TOPIC)
    all_ok = True
    for entry in entries:
        title = entry.get("title", "")
        body = entry.get("body", "")
        category = entry.get("category", "")
        cat_part = f"[{category}] " if category else ""
        payload = f"[{key}] obsidian {cat_part}{title}\n\n{body}"
        try:
            curl_cmd = ["curl", "-sL", "-d", payload, f"https://ntfy.sh/{topic}"]
            r = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=15)
            if r.returncode == 0:
                log(f"已发送: {title}")
            else:
                error(f"发送失败 ({title}): {r.stderr.strip()}")
                all_ok = False
        except subprocess.TimeoutExpired:
            error(f"发送超时 ({title})")
            all_ok = False
        except FileNotFoundError:
            error("未找到 curl 命令，请安装 curl")
            return False
    return all_ok


def send_markdown(entries: list[dict]) -> bool:
    path = Path("cognitive-log.md")
    with open(path, "a", encoding="utf-8") as f:
        for entry in entries:
            title = entry.get("title", "")
            body = entry.get("body", "")
            category = entry.get("category", "认知")
            f.write(f"## {title}\n\n")
            f.write(f"- **分类**: {category}\n")
            f.write(f"- **时间**: {entry.get('date', '')}\n\n")
            f.write(f"{body}\n\n---\n\n")
    log(f"已追加到 {path}")
    return True


SENDERS = {
    "obsidian-ntfy": send_obsidian_ntfy,
    "markdown": send_markdown,
    "none": lambda entries: (log(f"模拟模式: 将发送 {len(entries)} 条"), True),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="认知提取 — 存档时将认知收获推送到外部知识库")
    parser.add_argument("--backend", choices=BACKENDS, help="推送后端")
    parser.add_argument("--title", help="条目标题")
    parser.add_argument("--body", help="条目正文")
    parser.add_argument("--file", help="JSON 文件路径（包含条目列表或单条目）")
    args = parser.parse_args()

    entries = read_input(args)
    backend = get_backend(args)

    log(f"后端: {backend}, 条目数: {len(entries)}")

    sender = SENDERS.get(backend)
    ok = sender(entries)

    if ok:
        result(True, f"已发送 {len(entries)} 条")
        return 0
    else:
        result(False, "部分或全部发送失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
