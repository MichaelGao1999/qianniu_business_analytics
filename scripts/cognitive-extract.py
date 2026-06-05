#!/usr/bin/env python3
"""
认知提取脚本 — 将存档时的认知收获推送到外部知识库。

用法:
    python scripts/cognitive-extract.py --title "..." --body "..."
    python scripts/cognitive-extract.py --file <candidates.json>

后端（通过 --backend 或 COGNITIVE_EXTRACT_BACKEND 环境变量选择）:
    auto          自动选择: ntfy > obsidian-direct > markdown（默认）
    markdown      追加到 cognitive-log.md（零外部依赖）
    obsidian-ntfy 通过 ntfy.sh 推送到 Obsidian（需 OBSIDIAN_NTFY_KEY）
    obsidian-direct 直接写入 Obsidian vault 收件箱文件（仅 macOS）
    none          仅 stdout 打印，不发送

环境变量:
    COGNITIVE_EXTRACT_BACKEND   后端类型（默认: auto，自动选择最优可用后端）
    OBSIDIAN_NTFY_KEY           ntfy.sh 推送密钥（obsidian-ntfy 后端必需）
    NTFY_TOPIC                  ntfy.sh 主题（默认: cognitive-extract）

返回: exit code 0=成功, 1=部分失败, 2=输入错误
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


DEFAULT_NTFY_TOPIC = "cognitive-extract"
DEFAULT_BACKEND = "auto"
BACKENDS = ("auto", "markdown", "obsidian-ntfy", "obsidian-direct", "none")


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


def resolve_backend(backend: str) -> str:
    """Resolve 'auto' to concrete backend: ntfy > obsidian-direct > markdown."""
    if backend != "auto":
        return backend
    if os.environ.get("OBSIDIAN_NTFY_KEY"):
        return "obsidian-ntfy"
    vault = os.path.expanduser(
        "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/我的知识库"
    )
    inbox = os.path.join(vault, "🛠 技术搭建", "收件箱通道（ntfy.sh）收录的笔记.md")
    if os.path.exists(inbox):
        return "obsidian-direct"
    return "markdown"


def send_obsidian_ntfy(entries: list[dict], topic_override: str = "") -> bool:
    key = os.environ.get("OBSIDIAN_NTFY_KEY")
    if not key:
        error("obsidian-ntfy 后端需要 OBSIDIAN_NTFY_KEY 环境变量")
        return False
    topic = topic_override or os.environ.get("NTFY_TOPIC", DEFAULT_NTFY_TOPIC)
    url = f"https://ntfy.sh/{topic}"
    all_ok = True
    for entry in entries:
        title = entry.get("title", "")
        body = entry.get("body", "")
        category = entry.get("category", "")
        cat_part = f"[{category}] " if category else ""
        payload = f"[{key}] obsidian {cat_part}{title}\n\n{body}"
        try:
            if HAS_REQUESTS:
                r = requests.post(url, data=payload.encode("utf-8"),
                                  headers={"Content-Type": "text/plain; charset=utf-8"},
                                  timeout=15)
                if r.ok:
                    log(f"已发送: {title}")
                else:
                    error(f"发送失败 ({title}): HTTP {r.status_code} {r.text.strip()}")
                    all_ok = False
            else:
                import urllib.request
                req = urllib.request.Request(
                    url, data=payload.encode("utf-8"),
                    headers={"Content-Type": "text/plain; charset=utf-8"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    if resp.status == 200:
                        log(f"已发送: {title}")
                    else:
                        error(f"发送失败 ({title}): HTTP {resp.status}")
                        all_ok = False
        except Exception as e:
            error(f"发送失败 ({title}): {e}")
            all_ok = False
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


def send_obsidian_direct(entries: list[dict]) -> bool:
    """Write directly to Obsidian vault inbox file (macOS, bypasses ntfy)."""
    from datetime import datetime
    vault_path = os.path.expanduser(
        "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/我的知识库"
    )
    inbox_path = os.path.join(vault_path, "🛠 技术搭建", "收件箱通道（ntfy.sh）收录的笔记.md")
    if not os.path.exists(inbox_path):
        error(f"Obsidian vault 收件箱不存在: {inbox_path}")
        return False
    all_ok = True
    for entry in entries:
        title = entry.get("title", "")
        body = entry.get("body", "")
        category = entry.get("category", "认知")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        block = f"\n---\n\n### {title} · {now}\n> `{category}`\n\n{body}\n"
        try:
            with open(inbox_path, "a", encoding="utf-8") as f:
                f.write(block)
            log(f"已直写 Obsidian: {title}")
        except OSError as e:
            error(f"直写 Obsidian 失败 ({title}): {e}")
            all_ok = False
    return all_ok


SENDERS = {
    "markdown": send_markdown,
    "obsidian-direct": send_obsidian_direct,
    "none": lambda entries: (log(f"模拟模式: 将发送 {len(entries)} 条"), True),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="认知提取 — 存档时将认知收获推送到外部知识库")
    parser.add_argument("--backend", choices=BACKENDS, help="推送后端")
    parser.add_argument("--title", help="条目标题")
    parser.add_argument("--body", help="条目正文")
    parser.add_argument("--file", help="JSON 文件路径（包含条目列表或单条目）")
    parser.add_argument("--topic", help="ntfy.sh 主题（仅 obsidian-ntfy 后端，优先级高于 NTFY_TOPIC 环境变量）")
    args = parser.parse_args()

    entries = read_input(args)
    backend = resolve_backend(get_backend(args))

    log(f"后端: {backend}, 条目数: {len(entries)}")

    sender = SENDERS.get(backend)
    if backend == "obsidian-ntfy":
        ok = send_obsidian_ntfy(entries, topic_override=args.topic or "")
    else:
        ok = sender(entries)

    if ok:
        result(True, f"已发送 {len(entries)} 条")
        return 0
    else:
        result(False, "部分或全部发送失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
