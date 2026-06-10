#!/usr/bin/env python3
"""
统一经验索引生成脚本
解析 troubleshooting.md、lessons-learned.md、ADR.md，
自动生成 experience-index.md（统一搜索入口）。

用法:
    python scripts/build-experience-index.py
    python scripts/build-experience-index.py --check

--check 模式：验证索引与源文件是否同步（CI 用）
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional, Tuple


TROUBLE_FILE = "troubleshooting.md"
LESSONS_FILE = "lessons-learned.md"
DECISIONS_FILE = "ADR.md"
INDEX_FILE = "experience-index.md"

TECH_STACK_KEYWORDS: dict[str, list[str]] = {
    "Rust / Tauri": [
        "rust", "cargo", "tauri", "rustc", "crate", "webview2",
        "filetime", "getdiskfreespaceexw", "mingw", "ucrt", "dll",
        "0xc0000139", "0xc0000005", "status_entrypoint",
    ],
    "JavaScript / React / Vitest": [
        "javascript", "react", "jsx", "node", "npm", "vitest", "vite",
        "jest", "dom", "chess.js", "canvas", "svg", "queryselector",
        "queryselectorall", "addeventlistener", "event",
        "unexpected identifier", "cannot update",
    ],
    "Python": ["python", "pip", "pytest"],
    "网络 / 环境 / 权限": [
        "网络", "cdn", "dns", "代理", "proxy", "timeout", "连接超时",
        "防火墙", "firewall", "path", "编码", "utf", "权限",
        "中文路径", "huggingface", "modelscope", "github pages",
        "access is denied",
    ],
    "AI 工具链 / LLM": [
        "llm", "ollama", "llama", "llama-server", "model",
        "deepseek", "qwen", "gguf", "modelscope", "huggingface",
    ],
    "Git / GitHub": [
        "git", "github", "ssh", "push", "pull", "commit", "merge",
        "gh auth", "permission denied",
    ],
    "Windows / PowerShell": [
        "powershell", "windows", "ucrt", "dll", "mingw", "exe",
        "unexpectedtoken", "bom", "防火墙",
    ],
    "Chess / 引擎": [
        "stockfish", "chess", "uci", "pgn", "engine",
        "gomultipv", "candidate", "move",
    ],
}


def log(msg: str) -> None:
    print(f"[build-index] {msg}")


def infer_tech_stacks(text: str) -> list[str]:
    """根据文本推断技术栈标签"""
    text_lower = text.lower()
    text_lower = re.sub(r"https?://\S+", "", text_lower)
    stacks: list[str] = []
    for stack, keywords in TECH_STACK_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                stacks.append(stack)
                break
    return stacks if stacks else ["其他"]


def infer_domain(source: str, tags: list[str], category: str = "") -> str:
    """根据来源 + TAG 推断条目所属领域，用于新项目筛选"""
    s = source.lower()
    tags_lower = [t.lower() for t in tags]

    # 千牛 → python-data
    if "qianniu" in s or "天猫" in s:
        return "python-data"
    # blindfold-chess 的前端相关 → frontend
    if "blindfold" in s or "chess" in s:
        if any(t in tags_lower for t in ["dom", "i18n", "ux", "state-management"]):
            return "frontend"
        return "general"
    # french-exit → rust-tauri 或 frontend
    if "french-exit" in s or "tauri" in s or "rust" in tags_lower:
        if any(t in tags_lower for t in
               ["cross-platform", "state-management", "pagination", "security"]):
            return "rust-tauri"
        if "dom" in tags_lower or "ux" in tags_lower:
            return "frontend"
        return "general"
    # 母库/无来源/骨架自身 → infra 或 general
    if not source or s.startswith("母库") or "agent-coding-skeleton" in s:
        if any(t in tags_lower for t in
               ["project-structure", "indexing", "performance"]):
            return "infra"
        return "general"
    return "general"


# ── Troubleshooting 解析 ──

def extract_source_tag(text: str) -> tuple[str, str]:
    """从文本中提取 [来源:xxx] 或 [母库 @date] 标签（支持多个）"""
    sources = re.findall(r"\[来源:([^\]]+)\]", text)
    mothers = re.findall(r"\[母库[^\]]*\]", text)
    clean = re.sub(r"\s*\[来源:[^\]]+\]", "", text)
    clean = re.sub(r"\s*\[母库[^\]]*\]", "", clean).strip()
    all_sources = [s.strip() for s in sources] + [m.strip("[]") for m in mothers]
    source_str = " | ".join(all_sources) if all_sources else ""
    return clean, source_str


def parse_table_row(line: str) -> Optional[Tuple[str, str]]:
    """解析 Markdown 表格行"""
    if not line.startswith("|"):
        return None
    if re.match(r"^\|[-\s|:]+\|$", line):
        return None
    cells = [c.strip() for c in line.split("|")[1:-1]]
    if len(cells) < 2:
        return None
    field_name = re.sub(r"\*\*", "", cells[0]).strip()
    field_value = cells[1]
    if not field_name:
        return None
    return field_name, field_value


def normalize_status(raw: str) -> str:
    """将 troubleshooting.md 中非标准状态映射为标准枚举"""
    if not raw:
        return "—"
    s = raw.strip().replace("|", "").strip()
    mapping = {
        "已修复": "resolved",
        "已修复（测试已适配）": "resolved",
        "已修复（改为 IDE 串行）": "resolved",
        "已修复（有自动刷新机制）": "resolved",
        "已修复（有写入验证）": "resolved",
        "已解决": "resolved",
        "✅ 已修复": "resolved",
        "已知限制": "known_limitation",
        "已知未修复": "wont_fix",
        "已知未修复（逐步迁移中）": "wont_fix",
        "已知未修复（需用户侧配置）": "wont_fix",
        "已知未修复（业务侧问题）": "wont_fix",
        "已知未修复（需具体 case 分析）": "wont_fix",
        "已知未修复（不影响功能）": "known_limitation",
        "临时绕过": "wont_fix",
        "已知处理方案": "resolved",
        "待修复": "pending",
    }
    if s in mapping:
        return mapping[s]
    # fallback: 提取基础状态（如 "已修复（xxx）" → resolved）
    base = re.sub(r"[（(].*[）)]", "", s).strip()
    if base in mapping:
        return mapping[base]
    return s


def parse_troubleshooting(path: str) -> list[dict]:
    """解析 troubleshooting.md"""
    entries: list[dict] = []
    current_category = ""
    current_entry: Optional[dict] = None

    with open(path, "r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.rstrip("\n")

            if line.startswith("## ") and not line.startswith("### "):
                current_category = line[3:].strip()
                continue

            if line.startswith("### "):
                if current_entry:
                    entries.append(current_entry)
                title_line = line[4:].strip()
                title, source = extract_source_tag(title_line)
                current_entry = {
                    "type": "问题",
                    "category": current_category,
                    "title": title,
                    "source": source,
                    "domain": infer_domain(source, [], current_category),
                    "status": None,
                    "symptom": None,
                    "cause": None,
                    "solution": None,
                    "tags": [],
                    "module": "",
                    "line_start": line_no,
                    "file": TROUBLE_FILE,
                }
                continue

            if current_entry is None:
                continue

            parsed = parse_table_row(line)
            if parsed:
                field_name, field_value = parsed
                mapping = {
                    "状态": "status",
                    "现象": "symptom",
                    "原因": "cause",
                    "解决": "solution",
                }
                key = mapping.get(field_name)
                if key and current_entry.get(key) is None:
                    val = field_value
                    if key == "status":
                        val = normalize_status(field_value)
                    current_entry[key] = val

        if current_entry:
            entries.append(current_entry)

    # 去重：相同标题（去来源标签后）保留 resolved/promoted 超过 pending/wont_fix
    best: dict[str, dict] = {}
    RESOLVED_PRIORITY = {"resolved": 3, "promoted": 2, "known_limitation": 1, "pending": 0, "wont_fix": 0}
    for e in entries:
        key = e["title"].lower().strip()
        if key not in best:
            best[key] = e
        else:
            existing_prio = RESOLVED_PRIORITY.get(best[key].get("status", ""), 0)
            new_prio = RESOLVED_PRIORITY.get(e.get("status", ""), 0)
            if new_prio > existing_prio:
                best[key] = e
    unique = list(best.values())
    if len(unique) < len(entries):
        log(f"Dedup: {len(entries)} → {len(unique)} troubleshooting entries")
    return unique


# ── Lessons-learned 解析 ──

def parse_lessons_learned(path: str) -> list[dict]:
    """解析 lessons-learned.md"""
    entries: list[dict] = []

    # 按 | 数量选择对应的列数：4列(5个|) / 5列(6个|) / 6列(7个|)
    # P0: 5列标准 — | num | TAG:xxx | INFO/WARNING/CRITICAL | desc | module |
    P0_REGEX = r"^\|\s*(\d+)\s*\|\s*(TAG:\S+(?:\s+TAG:\S+)*)\s*\|\s*(INFO|WARNING|CRITICAL|TIP)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|$"
    # P1: 6列 — | num | TAG:xxx | 严重度 | desc | category | source |
    P1_REGEX = r"^\|\s*(\d+)\s*\|\s*(TAG:\S+(?:\s+TAG:\S+)*)\s*\|\s*(INFO|WARNING|CRITICAL|TIP)\s*\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$"
    # P2: 4列（无 TAG/severity）— | num | desc | category | source |
    P2_REGEX = r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*\[来源:([^\]]+)\].*?\|$"

    with open(path, "r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.rstrip("\n")

            pipe_count = line.count("|")
            m = None
            matched_pattern = None

            if pipe_count == 6:
                m = re.match(P0_REGEX, line)
                matched_pattern = 0 if m else None
            elif pipe_count == 7:
                m = re.match(P1_REGEX, line)
                matched_pattern = 1 if m else None
            elif pipe_count == 5:
                m = re.match(P2_REGEX, line)
                matched_pattern = 2 if m else None

            if not m:
                if pipe_count in (3, 4) and line.startswith("|") and not re.match(r"^\|[\s\-:|]+\|$", line):
                    log(f"  skipped {pipe_count}-column row at line {line_no} (fragment/duplicate)")
                continue

            num = m.group(1)
            desc = module = ""
            tags_str = ""
            severity = "INFO"
            tags: list[str] = []

            if matched_pattern == 0:
                # 5列标准格式
                tags_str = m.group(2).strip()
                severity = m.group(3).strip()
                desc = m.group(4).strip()
                module = m.group(5).strip()
                tags = re.findall(r"TAG:(\S+)", tags_str)
            elif matched_pattern == 1:
                # 6列（有 extra category + source 列）
                tags_str = m.group(2).strip()
                severity = m.group(3).strip()
                desc = m.group(4).strip()
                category = m.group(5).strip()
                source_col = m.group(6).strip()
                module = f"{category} / {source_col}" if category else source_col
                if source_col.startswith("[来源:") or source_col.startswith("[母库"):
                    desc = f"{desc} {source_col}"
                elif source_col:
                    desc = f"{desc} [来源:{source_col}]"
                tags = re.findall(r"TAG:(\S+)", tags_str)
            elif matched_pattern == 2:
                # 4列（无 TAG/severity）
                desc = m.group(2).strip()
                module = m.group(3).strip()
                # 重建来源标签，供 extract_source_tag 提取
                desc = f"{desc} [来源:{m.group(4).strip()}]"

            # 提取来源（从 desc 中提取 [来源:xxx] 标签）
            title_clean, source = extract_source_tag(desc)

            entries.append({
                "type": "经验",
                "category": " / ".join(tags) if tags else "未分类",
                "title": title_clean[:80] + ("..." if len(title_clean) > 80 else ""),
                "source": source,
                "domain": infer_domain(source, tags),
                "status": severity,
                "tags": tags,
                "module": module,
                "line_start": line_no,
                "file": LESSONS_FILE,
            })

    log(f"Parsed {len(entries)} entries from {LESSONS_FILE}")
    return entries


# ── Decisions 解析 ──

def parse_decisions(path: str) -> list[dict]:
    """解析 ADR.md"""
    entries: list[dict] = []

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # 匹配 ## ADR-xxx: 标题 [来源:...]
    pattern = r"^## (ADR-\d+[:：]\s*.+?)(?:\s*\[来源:([^\]]+)\])?\s*\n"
    for m in re.finditer(pattern, content, re.MULTILINE):
        adr_title = m.group(1).strip()
        source = m.group(2).strip() if m.group(2) else ""

        # 计算行号
        line_start = content[: m.start()].count("\n") + 1

        entries.append({
            "type": "决策",
            "category": "架构决策",
            "title": adr_title,
            "source": source,
            "domain": infer_domain(source, []),
            "status": "—",
            "tags": [],
            "module": "",
            "line_start": line_start,
            "file": DECISIONS_FILE,
        })

    return entries


# ── 索引生成 ──

def generate_index(
    trouble_entries: list[dict],
    lesson_entries: list[dict],
    decision_entries: list[dict],
) -> str:
    """生成统一索引 Markdown"""
    all_entries = trouble_entries + lesson_entries + decision_entries
    total = len(all_entries)

    lines: list[str] = [
        "# 经验索引",
        "",
        "> 本文件由 `scripts/build-experience-index.py` 自动生成。",
        "> 覆盖 troubleshooting / lessons-learned / ADR，统一搜索入口。",
        "",
        f"> 当前收录 **{total}** 条记录（问题 {len(trouble_entries)} + 经验 {len(lesson_entries)} + 决策 {len(decision_entries)}）。",
        "",
        "---",
        "",
        "## 快速搜索表",
        "",
        "| 领域 | 关键词 | 类型 | 分类 | 来源 | 状态 | 定位 |",
        "|------|--------|------|------|------|------|------|",
    ]

    for e in all_entries:
        status = (e.get("status") or "—").replace("|", "\\|")
        source = e.get("source", "—")
        source_short = source.split(" @")[0] if " @" in source else source
        category = e["category"] or "未分类"
        title_short = e["title"][:60] + ("..." if len(e["title"]) > 60 else "")
        domain = e.get("domain", "general")
        lines.append(
            f"| {domain} | {title_short} | {e['type']} | {category} | {source_short} | {status} | {e['file']}#L{e['line_start']} |"
        )

    # ── 按技术栈分组 ──
    lines.extend([
        "",
        "---",
        "",
        "## 按技术栈分组",
        "",
        "> 一个条目可能同时属于多个技术栈。",
        "",
    ])

    stack_map: dict[str, list[dict]] = {}
    for e in all_entries:
        text = f"{e['title']} {e.get('category', '')}"
        for stack in infer_tech_stacks(text):
            stack_map.setdefault(stack, []).append(e)

    preferred_order = [
        "Rust / Tauri",
        "JavaScript / React / Vitest",
        "Python",
        "AI 工具链 / LLM",
        "Git / GitHub",
        "网络 / 环境 / 权限",
        "Windows / PowerShell",
        "Chess / 引擎",
        "其他",
    ]
    sorted_stacks = sorted(
        stack_map.keys(),
        key=lambda s: (preferred_order.index(s) if s in preferred_order else 999, s),
    )

    for stack in sorted_stacks:
        lines.append(f"### {stack}")
        lines.append("")
        for e in stack_map[stack]:
            category = e["category"] or "未分类"
            lines.append(f"- [{e['type']}] {e['title'][:50]} — `{category}` → {e['file']}#L{e['line_start']}")
        lines.append("")

    # ── 按状态分组（troubleshooting 专用） ──
    trouble_by_status: dict[str, list[dict]] = {}
    for e in trouble_entries:
        status = e.get("status") or "—"
        trouble_by_status.setdefault(status, []).append(e)

    if trouble_by_status:
        lines.extend([
            "",
            "---",
            "",
            "## 按状态分组（troubleshooting）",
            "",
        ])
        status_order = ["pending", "resolved", "promoted", "wont_fix", "known_limitation", "—"]
        for status in status_order:
            items = trouble_by_status.get(status, [])
            if not items:
                continue
            lines.append(f"### {status}（{len(items)} 条）")
            lines.append("")
            for e in items[:20]:
                title_short = e["title"][:55] + ("..." if len(e["title"]) > 55 else "")
                lines.append(f"- {title_short} → {e['file']}#L{e['line_start']}")
            if len(items) > 20:
                lines.append(f"- ... 还有 {len(items) - 20} 条")
            lines.append("")

    # ── 按类型分组 ──
    lines.extend([
        "---",
        "",
        "## 按类型分组",
        "",
    ])

    type_map: dict[str, list[dict]] = {}
    for e in all_entries:
        type_map.setdefault(e["type"], []).append(e)

    for t in ["问题", "经验", "决策"]:
        items = type_map.get(t, [])
        if not items:
            continue
        lines.append(f"### {t}（{len(items)} 条）")
        lines.append("")
        for e in items[:20]:  # 每类最多显示 20 条
            title_short = e["title"][:55] + ("..." if len(e["title"]) > 55 else "")
            lines.append(f"- {title_short} → {e['file']}#L{e['line_start']}")
        if len(items) > 20:
            lines.append(f"- ... 还有 {len(items) - 20} 条")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build unified experience index")
    parser.add_argument("--check", action="store_true", help="Check if index is up-to-date")
    args = parser.parse_args()

    files = {
        TROUBLE_FILE: TROUBLE_FILE,
        LESSONS_FILE: LESSONS_FILE,
        DECISIONS_FILE: DECISIONS_FILE,
    }
    for name, path in files.items():
        if not Path(path).exists():
            log(f"WARNING: {path} not found, skipping")

    trouble_entries = []
    if Path(TROUBLE_FILE).exists():
        trouble_entries = parse_troubleshooting(TROUBLE_FILE)
        log(f"Parsed {len(trouble_entries)} entries from {TROUBLE_FILE}")

    lesson_entries = []
    if Path(LESSONS_FILE).exists():
        lesson_entries = parse_lessons_learned(LESSONS_FILE)

    decision_entries = []
    if Path(DECISIONS_FILE).exists():
        decision_entries = parse_decisions(DECISIONS_FILE)
        log(f"Parsed {len(decision_entries)} entries from {DECISIONS_FILE}")

    new_content = generate_index(trouble_entries, lesson_entries, decision_entries)

    if args.check:
        idx = Path(INDEX_FILE)
        if not idx.exists():
            log(f"ERROR: {INDEX_FILE} does not exist")
            return 1
        current = idx.read_text(encoding="utf-8")
        if current.strip() == new_content.strip():
            log("Index is up-to-date")
            return 0
        log("ERROR: Index is out of date. Run without --check to rebuild.")
        return 1

    Path(INDEX_FILE).write_text(new_content, encoding="utf-8")
    log(f"Wrote {INDEX_FILE} ({len(new_content)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
