#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过钉钉自定义机器人 Webhook 发送 markdown 消息（用于推送经营分析报告）。

技能要求：输入须为 **Markdown 源码**；推送的 **markdown 正文** 应与 **对话中发给用户的报告** 为 **同一套定稿**（同一 `-f` 文件或相同 stdin），勿单独写精简版，且对话与钉钉 **均为 Markdown**。

与本技能 **SKILL.md** 同级的 **scripts/** 目录（见上级 **README.md**）。

用法：
  # 必须：设置钉钉机器人 Webhook（未设置时脚本将跳过推送并提示）
  export DINGTALK_WEBHOOK='https://oapi.dingtalk.com/robot/send?access_token=...'
  cd .cursor/skills/jycm-fetch-report-analyze
  python3 scripts/dingtalk_send_markdown.py --title '上周全渠道经营复盘' -f report.md

  cat report.md | python3 scripts/dingtalk_send_markdown.py --title '经营周报'

从仓库根：python3 .cursor/skills/jycm-fetch-report-analyze/scripts/dingtalk_send_markdown.py ...

标题：钉钉消息标题 **必须包含「经营」**；若 `--title` 不含「经营」，脚本会自动加前缀 `经营·`。
安全：勿在日志中打印完整 URL。

钉钉单条 markdown 正文不宜过长，超长将自动截断并提示。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from constants import MAX_TEXT_DINGTALK as MAX_TEXT


def ensure_title_has_jingying(title: str) -> str:
    """钉钉推送标题必须含「经营」；缺失时自动补前缀。"""
    t = title.strip()
    if "经营" in t:
        return t
    return f"经营·{t}" if t else "经营分析报告"


def main() -> int:
    parser = argparse.ArgumentParser(description="钉钉机器人发送 markdown")
    parser.add_argument("--title", default="经营分析报告", help="消息标题（须含「经营」，否则自动补全）")
    parser.add_argument("--file", "-f", help="Markdown 正文文件；缺省则从 stdin 读")
    args = parser.parse_args()

    webhook = os.environ.get("DINGTALK_WEBHOOK", "").strip()
    if not webhook:
        print("未配置 DINGTALK_WEBHOOK，跳过钉钉推送。可通过 export DINGTALK_WEBHOOK='https://oapi.dingtalk.com/robot/send?access_token=...' 启用推送。")
        return 0
    title = ensure_title_has_jingying(args.title)

    if args.file:
        text = Path(args.file).expanduser().read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    text = text.strip()
    if len(text) > MAX_TEXT:
        text = text[: MAX_TEXT - 80] + "\n\n...(内容过长已截断，请分段发送或改用文件链接)"

    body = {
        "msgtype": "markdown",
        "markdown": {"title": title[:50], "text": text},
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

    if out.get("errcode") != 0:
        print(json.dumps(out, ensure_ascii=False), file=sys.stderr)
        return 1

    print("ok", out.get("errmsg", ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
