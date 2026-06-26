#!/usr/bin/env python3
"""
跨仓库 session-log 按日期聚合提取脚本。

遍历 config/downstream-projects.json 中所有项目的 session-log.md，
按「## YYYY-MM-DD」切分段落，提取指定日期记录打印到 stdout。
本地路径不存在时通过 GitHub raw 回退（gh CLI，支持 private 仓库）。

用法:
    python scripts/aggregate-sessions.py                    # 当天
    python scripts/aggregate-sessions.py --date 2026-06-20  # 指定日期
    python scripts/aggregate-sessions.py --date 昨天        # 自然语言日期
    python scripts/aggregate-sessions.py --since 2026-06-16 # 从某天开始
    python scripts/aggregate-sessions.py --since 2026-06-16 --until 2026-06-23  # 范围

依赖: 纯 stdlib，零外部依赖。GitHub raw 回退需要 gh CLI。
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import List, Optional, Tuple, cast
from urllib.parse import quote

# ── 路径 ──────────────────────────────────────────────────────

CONFIG_PATH = "config/downstream-projects.json"
GITHUB_SYNC_CONFIG = "config/github-sync.json"
SESSION_LOG = "session-log.md"
# 母库自身（不在 downstream-projects.json 中）
MOTHER_REPO = ("ai-workbench", str(Path(__file__).resolve().parent.parent))
# session-log 日期标题正则: "## YYYY-MM-DD" 或 "## YYYY-MM-DD — 标题"
DATE_PATTERN = re.compile(r"^## (\d{4}-\d{2}-\d{2})")

# ── GitHub raw 缓存 ───────────────────────────────────────────

_raw_cache: dict[str, Optional[str]] = {}


# ── 自然语言日期解析 ──────────────────────────────────────────

_CHINESE_DIGITS = {
    "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
    "两": 2,
}

_NUM_PATTERN = re.compile(r"(\d+)天前")
_CHINESE_NUM_PATTERN = re.compile(r"([一二三四五六七八九两])天前")


def _chinese_to_int(text: str) -> Optional[int]:
    if len(text) == 1:
        return _CHINESE_DIGITS.get(text)
    return None


def parse_date_natural(text: str, ref: Optional[date] = None) -> Optional[date]:
    """解析自然语言日期文本，返回 date 或 None。"""
    ref = ref or date.today()

    text = text.strip()

    # 标准 ISO
    try:
        return date.fromisoformat(text)
    except ValueError:
        pass

    # 精确中英文关键词
    mapping = {
        "今天": 0, "today": 0,
        "昨天": -1, "yesterday": -1,
        "前天": -2,
    }
    if text in mapping:
        return ref + timedelta(days=mapping[text])

    # "N天前" / "N天前"
    m = _NUM_PATTERN.match(text)
    if m:
        return ref - timedelta(days=int(m.group(1)))
    m = _CHINESE_NUM_PATTERN.match(text)
    if m:
        n = _chinese_to_int(m.group(1))
        if n is not None:
            return ref - timedelta(days=n)

    # "X月X号" / "X月X日"（当前年）
    m = re.match(r"(\d{1,2})月(\d{1,2})[号日]", text)
    if m:
        try:
            return date(ref.year, int(m.group(1)), int(m.group(2)))
        except ValueError:
            return None

    return None


def resolve_dates(target_date: Optional[str],
                  since: Optional[str],
                  until: Optional[str]) -> List[date]:
    """将命令行日期参数解析为 date 对象列表（含 when 语义）。"""
    ref = date.today()

    if target_date:
        d = parse_date_natural(target_date, ref)
        return [d] if d else []

    start = since
    end = until

    if start:
        d_start = parse_date_natural(start, ref)
        if not d_start:
            return []
        if end:
            d_end = parse_date_natural(end, ref)
            if not d_end or d_end < d_start:
                return []
            return [d_start + timedelta(days=i)
                    for i in range((d_end - d_start).days + 1)]
        # 只有 since → 从该天到今天
        return [d_start + timedelta(days=i)
                for i in range((ref - d_start).days + 1)]

    # 无参数 → 今天
    return [ref]


# ── GitHub 配置读取 ───────────────────────────────────────────

def _load_username() -> Optional[str]:
    """从 github-sync.json 读取 username，不存在/解析失败返回 None。"""
    config_file = Path(GITHUB_SYNC_CONFIG)
    if not config_file.exists():
        return None
    try:
        with open(GITHUB_SYNC_CONFIG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return cast(Optional[str], cfg.get("username"))
    except (json.JSONDecodeError, IOError, KeyError):
        return None


def get_default_branch(owner: str, repo: str) -> Optional[str]:
    """通过 gh api 获取仓库默认分支。"""
    cache_key = f"branch:{owner}/{repo}"
    if cache_key in _raw_cache:
        return _raw_cache[cache_key]
    try:
        result = subprocess.run(
            ["gh", "api", f"/repos/{owner}/{repo}", "--jq", ".default_branch"],
            capture_output=True, encoding="utf-8", timeout=15,
        )
        if result.returncode == 0:
            branch = result.stdout.strip()
            _raw_cache[cache_key] = branch
            return branch
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    # fallback
    _raw_cache[cache_key] = "main"
    return "main"


def fetch_from_github(owner: str, repo: str, filepath: str,
                      branch: str = "main") -> Optional[str]:
    """通过 gh CLI 从 GitHub 拉取文件内容（支持 private 仓库）。

    返回文件文本内容，文件不存在时返回 None。
    """
    cache_key = f"raw:{owner}/{repo}/{filepath}@{branch}"
    if cache_key in _raw_cache:
        return _raw_cache[cache_key]

    encoded_path = quote(filepath)
    url = f"/repos/{owner}/{repo}/contents/{encoded_path}?ref={branch}"
    try:
        result = subprocess.run(
            ["gh", "api", url, "-H", "Accept: application/vnd.github.raw"],
            capture_output=True, encoding="utf-8", timeout=15,
        )
        if result.returncode == 0:
            _raw_cache[cache_key] = result.stdout
            return result.stdout
        # 404 = 文件不存在
        if "Not Found" in result.stderr:
            _raw_cache[cache_key] = None
            return None
        print(f"[warning] gh api 失败 [{repo}]: {result.stderr.strip()}", file=sys.stderr)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"[warning] gh CLI 不可用 [{repo}]: {e}", file=sys.stderr)

    _raw_cache[cache_key] = None
    return None


# ── 仓库发现 ──────────────────────────────────────────────────

def load_downstream_projects(config_path: str) -> List[Tuple[str, Path]]:
    """从 downstream-projects.json 读取项目列表。"""
    projects: List[Tuple[str, Path]] = []

    config_file = Path(config_path)
    if not config_file.exists():
        print(f"[warning] 未找到 {config_path}", file=sys.stderr)
        return projects

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    for p in cfg.get("projects", []):
        name = p.get("name", "unknown")
        paths = p.get("paths", {})
        local_path = paths.get("darwin") or paths.get("win32")
        if not local_path:
            continue
        # 展开 ~
        local_path = os.path.expanduser(local_path)
        projects.append((name, Path(local_path)))

    return projects


def get_all_repos() -> List[Tuple[str, Optional[Path], Optional[str], Optional[str]]]:
    """返回所有仓库信息：(名称, 本地路径, GitHub owner, GitHub repo 名)。

    本地路径不存在时为 None，owner 读取不到时为 None（跳过 GitHub 回退）。
    """
    repos: List[Tuple[str, Optional[Path], Optional[str], Optional[str]]] = []

    # GitHub owner
    owner = _load_username()

    # 母库
    mother_path_str = os.path.expanduser(MOTHER_REPO[1])
    mother_path = Path(mother_path_str).resolve()
    repos.append((MOTHER_REPO[0], mother_path, owner, MOTHER_REPO[0]))

    # 下游
    config_file = Path(os.path.dirname(os.path.abspath(__file__))) / ".." / CONFIG_PATH
    for name, path in load_downstream_projects(str(config_file.resolve())):
        repos.append((name, path, owner, name))

    return repos


# ── session-log 解析 ──────────────────────────────────────────

def parse_sections(text: str) -> List[Tuple[str, str]]:
    """按 ## YYYY-MM-DD 切分文本，返回 [(日期, 原始段落内容)]。"""
    sections: List[Tuple[str, str]] = []
    lines = text.split("\n")
    current_date: Optional[str] = None
    current_lines: List[str] = []

    for line in lines:
        m = DATE_PATTERN.match(line)
        if m:
            if current_date and current_lines:
                sections.append((current_date, "\n".join(current_lines).strip()))
            current_date = m.group(1)
            current_lines = []
        else:
            if current_date:
                current_lines.append(line)

    # 最后一段
    if current_date and current_lines:
        sections.append((current_date, "\n".join(current_lines).strip()))

    return sections


def parse_session_log(log_path: Path) -> List[Tuple[str, str]]:
    """从本地 session-log.md 文件解析段落。"""
    if not log_path.exists():
        return []
    with open(log_path, "r", encoding="utf-8") as f:
        return parse_sections(f.read())


# ── 输出 ──────────────────────────────────────────────────────

_MD_PATTERNS = [
    (re.compile(r'\*\*(.+?)\*\*'), r'\1'),      # **bold**
    (re.compile(r'\*(.+?)\*'), r'\1'),           # *italic*
    (re.compile(r'`(.+?)`'), r'\1'),             # `code`
    (re.compile(r'^#+\s*', re.MULTILINE), ''),   # ## headers
]


def _strip_markdown(text: str) -> str:
    """去除 Markdown 格式符号，保留纯文本。"""
    for pattern, repl in _MD_PATTERNS:
        text = pattern.sub(repl, text)
    return text.strip()


def _extract_summary(body: str) -> str:
    """从原始 session-log 段落中提取摘要文本；无摘要时返回原文。"""
    lines = body.split("\n")
    summary_lines: List[str] = []

    in_execution = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("**用户指令**"):
            summary_lines.append(f"📋 {stripped.replace('**用户指令**：', '').replace('**用户指令**:', '').strip()}")
        elif stripped.startswith("**实际执行**"):
            in_execution = True
        elif stripped.startswith("**变更文件**"):
            break
        elif stripped.startswith("**关键决策**"):
            break
        elif stripped.startswith("**关键发现**"):
            break
        elif stripped == "---":
            break
        elif in_execution and stripped:
            if stripped.startswith("1.") or stripped.startswith("2.") or \
               stripped.startswith("3.") or stripped.startswith("4.") or \
               stripped.startswith("5.") or stripped.startswith("6.") or \
               stripped.startswith("- "):
                stripped_clean = re.sub(r'^(\d+\.\s*|-\s*)', '', stripped).strip()
                summary_lines.append(f"  - {stripped_clean}")
            elif not stripped.startswith("   "):
                break

    if summary_lines:
        lines_text = "\n".join(summary_lines)
        return _strip_markdown(lines_text)
    else:
        return _strip_markdown(body)


def format_entry(body: str) -> str:
    """格式化单条日记条目（无项目标头）。"""
    return _extract_summary(body)


# ── 主入口 ─────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="跨仓库 session-log 按日期聚合提取",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "日期参数支持:\n"
            "  ISO格式: 2026-06-20\n"
            "  自然语言: 今天, 昨天, 前天, 3天前, 三天前, 6月20号\n\n"
            "示例:\n"
            "  %(prog)s                    # 今天\n"
            "  %(prog)s --date 昨天        # 昨天\n"
            "  %(prog)s --date 2026-06-20  # 指定日期\n"
            "  %(prog)s --since 本周一     # 本周开始到今天\n"
        ),
    )
    parser.add_argument("--date", help="目标日期（ISO 或自然语言）")
    parser.add_argument("--since", help="起始日期（范围模式）")
    parser.add_argument("--until", help="结束日期（范围模式，默认今天）")
    args = parser.parse_args()

    # 解析目标日期
    target_dates = resolve_dates(args.date, args.since, args.until)
    if not target_dates:
        print("[error] 无法解析日期参数", file=sys.stderr)
        sys.exit(1)

    target_set = {d.isoformat() for d in target_dates}

    # 发现仓库
    repos = get_all_repos()
    found_any = False

    for repo_name, repo_path, gh_owner, gh_repo in repos:
        sections: List[Tuple[str, str]] = []

        # 优先读取本地文件
        if repo_path is not None and (repo_path / SESSION_LOG).exists():
            sections = parse_session_log(repo_path / SESSION_LOG)
        elif gh_owner and gh_repo:
            # GitHub raw 回退
            branch = get_default_branch(gh_owner, gh_repo) or "main"
            raw_text = fetch_from_github(gh_owner, gh_repo, SESSION_LOG, branch)
            if raw_text:
                sections = parse_sections(raw_text)

        matched = [(d, b) for d, b in sections if d in target_set]

        if not matched:
            continue

        # 输出：一次项目标头 + 下面所有条目
        if not found_any:
            found_any = True  # 只在首次有内容时标记
        print(f"=== {repo_name} ===")
        for _, body in matched:
            print(format_entry(body))
            print()
        print()

    if not found_any:
        print("[info] 未找到匹配日期的工作记录", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
