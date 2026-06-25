"""Shared merge logic for syncing knowledge files (lessons + troubleshooting).

Used by both sync-knowledge.py (aggregation) and distribute.py (distribution).
Both directions share the same dedup skeleton: exact match → similarity > 0.75 skip → insert.
"""

import re
from datetime import datetime
from typing import Tuple

from utils import similarity, clean_source_tag


def merge_lessons(
    text: str, entries: list[dict], source_name: str,
    threshold: float = 0.75,
) -> Tuple[str, int, int]:
    """Merge lessons entries into Markdown text (lessons-learned.md format).

    Args:
        text: Existing file content
        entries: Parsed entries from markdown_parser.parse_lessons()
        source_name: Label for the source tag (repo name or "AI Workbench")

    Returns:
        (new_text, added_count, skipped_count)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    source_tag = f"[来源:{source_name} @{today}]"
    added = 0
    skipped = 0

    existing_descs = re.findall(
        r"^\|\s*\|\s*(.+?)\s*(?:\[来源:.+?\])?\s*\|",
        text,
        re.MULTILINE,
    )

    lines_to_add = []
    for e in entries:
        desc = e["description"]
        if not desc or (desc.startswith("[") and desc.endswith("]")):
            continue

        # exact match
        if desc in text:
            skipped += 1
            continue

        # similarity dedup
        dup = False
        for existing in existing_descs:
            existing_clean = re.sub(r"\[来源:.+?\]", "", existing).strip()
            if existing_clean and similarity(desc, existing_clean) > threshold:
                skipped += 1
                dup = True
                break
        if dup:
            continue

        line = f"| | {desc} {source_tag} | {e.get('source', '')} |"
        lines_to_add.append(line)
        added += 1

    if not lines_to_add:
        return text, 0, skipped

    # find last table line to insert after
    last_table_line_end = -1
    for m in re.finditer(r"^\|.*\|\s*$", text, re.MULTILINE):
        last_table_line_end = m.end()

    if last_table_line_end == -1:
        new_text = text.rstrip() + "\n" + "\n".join(lines_to_add) + "\n"
    else:
        insert_pos = last_table_line_end
        new_text = (
            text[:insert_pos]
            + "\n"
            + "\n".join(lines_to_add)
            + "\n"
            + text[insert_pos:]
        )

    return new_text, added, skipped


def merge_troubleshooting(
    text: str, entries: list[dict], source_name: str,
    threshold: float = 0.85,
) -> Tuple[str, int, int]:
    """Merge troubleshooting entries into Markdown text (troubleshooting.md format).

    Args:
        text: Existing file content
        entries: Parsed entries from markdown_parser.parse_troubleshooting()
        source_name: Label for the source tag (repo name or "AI Workbench")

    Returns:
        (new_text, added_count, skipped_count)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    source_tag = f"[来源:{source_name} @{today}]"
    added = 0
    skipped = 0

    existing_keywords = re.findall(r"^###\s+(.+?)$", text, re.MULTILINE)

    blocks = []
    for e in entries:
        keyword_clean = clean_source_tag(e["keyword"])

        # exact match
        if keyword_clean in text:
            skipped += 1
            continue

        # similarity dedup
        dup = False
        for existing in existing_keywords:
            existing_clean = clean_source_tag(existing)
            if existing_clean and similarity(keyword_clean, existing_clean) > threshold:
                skipped += 1
                dup = True
                break
        if dup:
            continue

        new_block = f"### {keyword_clean} {source_tag}\n\n{e['body']}\n"
        blocks.append(new_block)
        added += 1

    if not blocks:
        return text, 0, skipped

    separator = "\n---\n\n" if text.strip() else ""
    new_text = text.rstrip() + separator + "\n".join(blocks)
    return new_text, added, skipped
