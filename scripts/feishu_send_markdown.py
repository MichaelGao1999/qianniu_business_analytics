#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过飞书自定义机器人 Webhook 发送 Markdown 消息（用于推送经营分析报告）。

用法：
  export FEISHU_WEBHOOK='https://open.feishu.cn/open-apis/bot/v2/hook/...'
  python3 scripts/feishu_send_markdown.py --title '上周经营复盘' -f report.md

  cat report.md | python3 scripts/feishu_send_markdown.py --title '经营周报'

标题：消息标题 **必须包含「经营」**；若 `--title` 不含「经营」，脚本会自动加前缀 `经营·`。
安全：勿在日志中打印完整 URL。

飞书 text 类型单条消息内容不宜过长，超长将自动截断并提示。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from constants import MAX_TEXT_FEISHU as MAX_TEXT


def ensure_title_has_jingying(title: str) -> str:
    """推送标题必须含「经营」；缺失时自动补前缀。"""
    t = title.strip()
    if "经营" in t:
        return t
    return f"经营·{t}" if t else "经营分析报告"


def main() -> int:
    parser = argparse.ArgumentParser(description="飞书机器人发送 markdown")
    parser.add_argument("--title", default="经营分析报告", help="消息标题（须含「经营」，否则自动补全）")
    parser.add_argument("--file", "-f", help="Markdown 正文文件；缺省则从 stdin 读")
    args = parser.parse_args()

    webhook = os.environ.get("FEISHU_WEBHOOK", "").strip()
    if not webhook:
        print("未配置 FEISHU_WEBHOOK，跳过飞书推送。可通过 export FEISHU_WEBHOOK='https://open.feishu.cn/open-apis/bot/v2/hook/...' 启用推送。")
        return 0
    title = ensure_title_has_jingying(args.title)

    if args.file:
        text = Path(args.file).expanduser().read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    text = text.strip()
    if len(text) > MAX_TEXT:
        text = text[: MAX_TEXT - 80] + "\n\n...(内容过长已截断，请查看完整报告文件)"

    # 飞书 text 类型：将标题和内容拼接发送
    full_text = f"**{title}**\n\n{text}"

    body = {
        "msg_type": "text",
        "content": {
            "text": full_text
        },
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}", file=sys.stderr)
        print(e.read().decode("utf-8", errors="replace")[:500], file=sys.stderr)
        return 1

    try:
        out = json.loads(raw)
    except json.JSONDecodeError:
        print(raw[:500], file=sys.stderr)
        return 1

    if out.get("code") != 0:
        print(json.dumps(out, ensure_ascii=False), file=sys.stderr)
        return 1

    print("ok", out.get("msg", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
