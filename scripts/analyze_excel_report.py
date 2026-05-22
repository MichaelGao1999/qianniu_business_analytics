#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生意参谋 Excel 经营分析报告生成器

用法:
  python3 scripts/analyze_excel_report.py data/店铺.xlsx
  python3 scripts/analyze_excel_report.py data/店铺A.xlsx data/店铺B.xlsx --shop "多店合并"
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

BJ_TZ = timezone(timedelta(hours=8))

# 核心指标关键词映射
METRIC_KEYWORDS: Dict[str, List[str]] = {
    "日期": ["日期", "时间", "date", "day"],
    "店铺": ["店铺", "店铺名称", "店铺名", "shop"],
    "商品": ["商品", "商品名称", "商品名", "item"],
    "访客数": ["访客数", "浏览量", "uv", "访客", "流量"],
    "支付金额": ["支付金额", "成交金额", "gmv", "交易额", "成交金额(元)", "支付金额(元)"],
    "支付转化率": ["支付转化率", "转化率", "成交转化率", "下单转化率"],
    "加购人数": ["加购人数", "加入购物车人数", "加购", "购物车人数"],
    "支付买家数": ["支付买家数", "支付人数", "成交人数", "买家数", "付款人数"],
    "客单价": ["客单价", "人均客单价", "笔单价"],
    "退款金额": ["退款金额", "退款", "退货金额"],
    "搜索访客数": ["搜索访客数", "搜索流量", "搜索uv"],
    "直通车花费": ["直通车花费", "直通车", "ppc花费"],
    "钻展花费": ["钻展花费", "钻展"],
}


def find_column(df: pd.DataFrame, keywords: List[str]) -> Optional[str]:
    """在 DataFrame 列名中模糊匹配关键词。"""
    cols_lower = {c.lower(): c for c in df.columns}
    for kw in keywords:
        kw_lower = kw.lower()
        for lower_col, original_col in cols_lower.items():
            if kw_lower in lower_col:
                return original_col
    return None


def find_columns(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    """为所有核心指标查找对应的列名。"""
    return {metric: find_column(df, kws) for metric, kws in METRIC_KEYWORDS.items()}


def detect_date_column(df: pd.DataFrame) -> Optional[str]:
    """检测日期列。"""
    col = find_column(df, METRIC_KEYWORDS["日期"])
    if col:
        return col
    for c in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[c]):
            return c
    return None


def parse_date_column(series: pd.Series) -> pd.Series:
    """尝试将列解析为日期。"""
    try:
        return pd.to_datetime(series, errors="coerce")
    except Exception:
        return pd.Series([None] * len(series))


def fmt_number(val: Any) -> str:
    """格式化数值。"""
    if val is None or pd.isna(val):
        return "-"
    if isinstance(val, (int, float)):
        if isinstance(val, int) or float(val).is_integer():
            return f"{int(val):,}"
        return f"{val:,.2f}"
    return str(val)


def fmt_currency(val: Any) -> str:
    """格式化为货币。"""
    if val is None or pd.isna(val):
        return "-"
    if isinstance(val, (int, float)):
        return f"¥{val:,.2f}"
    return str(val)


def fmt_percent(val: Any) -> str:
    """格式化为百分比。"""
    if val is None or pd.isna(val):
        return "-"
    if isinstance(val, (int, float)):
        if abs(val) < 1:
            return f"{val * 100:.2f}%"
        return f"{val:.2f}%"
    return str(val)


def smart_fmt(col_name: str, val: Any) -> str:
    """根据列名智能格式化数值。"""
    name_lower = str(col_name).lower()
    if any(k in name_lower for k in ["金额", "gmv", "单价", "花费", "价格"]):
        return fmt_currency(val)
    if any(k in name_lower for k in ["率", "转化", "占比"]):
        return fmt_percent(val)
    return fmt_number(val)


def read_excel_file(path: Path) -> Dict[str, pd.DataFrame]:
    """读取 Excel 文件，返回 {sheet_name: DataFrame}。"""
    try:
        xls = pd.ExcelFile(path)
        return {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in xls.sheet_names}
    except Exception as e:
        raise ValueError(f"无法读取 Excel 文件 {path}: {e}")


def analyze_sheets(sheets: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """分析所有 sheet，识别结构和核心数据。"""
    result = {"summary_sheet": None, "detail_sheet": None, "top_sheet": None, "sheets_info": []}

    for name, df in sheets.items():
        info = {
            "name": name,
            "shape": df.shape,
            "columns": list(df.columns),
            "date_col": detect_date_column(df),
            "shop_col": find_column(df, METRIC_KEYWORDS["店铺"]),
            "item_col": find_column(df, METRIC_KEYWORDS["商品"]),
            "metrics": find_columns(df),
        }
        result["sheets_info"].append(info)

        if info["date_col"] and info["shape"][0] > 1:
            if result["detail_sheet"] is None or info["shape"][0] > result["detail_sheet"]["shape"][0]:
                result["detail_sheet"] = info
        elif info["shop_col"] or info["item_col"]:
            if result["top_sheet"] is None:
                result["top_sheet"] = info
        elif result["summary_sheet"] is None:
            result["summary_sheet"] = info

    if result["detail_sheet"] is None and result["summary_sheet"]:
        result["detail_sheet"] = result["summary_sheet"]

    return result


def build_summary_table(df: pd.DataFrame, info: Dict[str, Any]) -> List[Tuple[str, str]]:
    """从整体指标 sheet 中提取关键指标表格数据。"""
    rows = []
    metrics = info["metrics"]
    priority = ["访客数", "支付金额", "支付买家数", "支付转化率", "客单价", "加购人数"]
    for metric in priority:
        col = metrics.get(metric)
        if col and col in df.columns:
            val = df[col].iloc[-1] if len(df) > 0 else None
            rows.append((metric, smart_fmt(col, val)))

    for col in df.columns:
        if col in [m for m in metrics.values() if m]:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            val = df[col].iloc[-1] if len(df) > 0 else None
            rows.append((col, smart_fmt(col, val)))

    return rows[:12]


def build_trend_table(df: pd.DataFrame, info: Dict[str, Any]) -> Tuple[List[str], List[List[str]]]:
    """从明细 sheet 中提取日度趋势表格。"""
    date_col = info["date_col"]
    if not date_col:
        return [], []

    df = df.copy()
    df[date_col] = parse_date_column(df[date_col])
    df = df.dropna(subset=[date_col]).sort_values(by=date_col)

    numeric_cols = []
    priority = ["访客数", "支付金额", "支付转化率", "支付买家数", "客单价", "加购人数"]
    metrics = info["metrics"]
    for metric in priority:
        col = metrics.get(metric)
        if col and col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)

    for col in df.columns:
        if col == date_col or col in numeric_cols:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)

    numeric_cols = numeric_cols[:6]
    headers = ["日期"] + numeric_cols
    rows = []
    for _, row in df.iterrows():
        d = row[date_col]
        date_str = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)[:10]
        vals = [smart_fmt(col, row[col]) for col in numeric_cols]
        rows.append([date_str] + vals)

    return headers, rows


def build_top_table(df: pd.DataFrame, info: Dict[str, Any]) -> Tuple[Optional[str], List[str], List[List[str]]]:
    """从明细 sheet 中提取 TOP N 排行。"""
    shop_col = info["shop_col"]
    item_col = info["item_col"]
    date_col = info["date_col"]
    dim_col = item_col or shop_col
    if not dim_col:
        return None, [], []

    metrics = info["metrics"]
    amount_col = metrics.get("支付金额")
    if not amount_col or amount_col not in df.columns:
        for col in df.columns:
            if col != dim_col and col != date_col and pd.api.types.is_numeric_dtype(df[col]):
                amount_col = col
                break

    if not amount_col:
        return dim_col, [], []

    grouped = df.groupby(dim_col)[amount_col].sum().reset_index()
    grouped = grouped.sort_values(by=amount_col, ascending=False).head(10)

    headers = [dim_col, amount_col]
    rows = []
    for _, row in grouped.iterrows():
        rows.append([str(row[dim_col])[:30], smart_fmt(amount_col, row[amount_col])])

    return dim_col, headers, rows


def generate_insights(
    summary_rows: List[Tuple[str, str]],
    headers: List[str],
    trend_rows: List[List[str]],
    top_dim: Optional[str],
    top_rows: List[List[str]],
) -> List[str]:
    """基于数据自动生成分析总结（3~6条量化要点）。"""
    insights = []

    amount_val = None
    visitor_val = None
    for label, val in summary_rows:
        if any(k in label for k in ["支付金额", "成交", "gmv"]):
            amount_val = val
        if "访客" in label:
            visitor_val = val

    if amount_val:
        insights.append(f"统计周期内店铺支付金额达 **{amount_val}**，整体经营规模可观。")
    if visitor_val:
        insights.append(f"全周期访客数为 **{visitor_val}**，流量基础稳固。")

    if len(trend_rows) >= 2:
        amount_idx = None
        for i, h in enumerate(headers):
            if any(k in h for k in ["金额", "成交", "gmv"]):
                amount_idx = i
                break

        if amount_idx is not None:
            try:
                first_s = trend_rows[0][amount_idx].replace("¥", "").replace(",", "")
                last_s = trend_rows[-1][amount_idx].replace("¥", "").replace(",", "")
                first_val = float(first_s) if first_s != "-" else 0
                last_val = float(last_s) if last_s != "-" else 0
                if first_val > 0:
                    change = (last_val - first_val) / first_val * 100
                    trend_word = "上升" if change > 0 else "下滑"
                    insights.append(f"周期首尾对比，支付金额 {trend_word} **{abs(change):.1f}%**，{'呈增长态势' if change > 0 else '需关注后续走势'}。")
            except Exception:
                pass

    if len(trend_rows) >= 3:
        insights.append(f"统计周期共 **{len(trend_rows)} 天**，日度数据完整，可用于进一步做同比/环比分析。")

    if top_rows:
        top_name = top_rows[0][0] if top_rows else ""
        top_val = top_rows[0][1] if top_rows else ""
        insights.append(f"{top_dim or '商品'}维度排行中，**{top_name}** 以 **{top_val}** 位居首位，是核心贡献项。")

    for label, val in summary_rows:
        if "转化率" in label and val != "-":
            insights.append(f"整体支付转化率为 **{val}**，建议结合流量结构和商品详情页做进一步诊断。")
            break

    seen = set()
    unique = []
    for ins in insights:
        if ins not in seen:
            seen.add(ins)
            unique.append(ins)

    return unique[:6]


def generate_report(excel_paths: List[Path], shop_name: Optional[str] = None, output_path: Optional[Path] = None) -> Path:
    """生成四段式 Markdown 经营分析报告。"""
    if not excel_paths:
        raise ValueError("未提供 Excel 文件")

    # 读取并分析所有 Excel
    all_sheets = {}
    all_analysis = []
    for path in excel_paths:
        sheets = read_excel_file(path)
        all_sheets[str(path)] = sheets
        all_analysis.append(analyze_sheets(sheets))

    primary_sheets = list(all_sheets.values())[0]
    primary_analysis = all_analysis[0]
    primary_detail = primary_analysis["detail_sheet"]
    primary_df = primary_sheets[primary_detail["name"]] if primary_detail else None
    top_detail = primary_analysis["top_sheet"]
    top_df = primary_sheets[top_detail["name"]] if top_detail else None

    # 推断店铺名称
    if not shop_name:
        fname = excel_paths[0].stem
        m = re.match(r"(.+?)_\d{8}(_\d{8})?", fname)
        shop_name = m.group(1) if m else fname

    # 推断日期范围
    date_range_str = ""
    if primary_df is not None and primary_detail and primary_detail["date_col"]:
        date_col = primary_detail["date_col"]
        dates = parse_date_column(primary_df[date_col]).dropna()
        if len(dates) > 0:
            date_range_str = f"{dates.min().strftime('%Y%m%d')}_{dates.max().strftime('%Y%m%d')}"
    if not date_range_str:
        date_range_str = datetime.now(BJ_TZ).strftime("%Y%m%d")

    # 构建报告
    lines = []
    lines.append(f"# {shop_name} 经营分析报告")
    lines.append("")
    lines.append(f"> 统计周期：{date_range_str.replace('_', ' 至 ')} ｜ 数据来源：生意参谋导出Excel ｜ 生成时间：{datetime.now(BJ_TZ).strftime('%Y-%m-%d %H:%M')}")

    lines.append("")

    # 一、整体指标
    lines.append("## 一、整体指标")
    lines.append("")
    summary_rows = []
    if primary_df is not None and primary_detail:
        summary_rows = build_summary_table(primary_df, primary_detail)

    if summary_rows:
        lines.append("| 指标 | 数值 |")
        lines.append("|------|------|")
        for label, val in summary_rows:
            lines.append(f"| {label} | {val} |")
    else:
        lines.append("> 未能自动识别汇总指标，请检查 Excel 列名是否包含常见指标（如访客数、支付金额、转化率等）。")
    lines.append("")

    # 二、日度趋势
    lines.append("## 二、日度趋势")
    lines.append("")
    trend_headers, trend_rows = [], []
    if primary_df is not None and primary_detail:
        trend_headers, trend_rows = build_trend_table(primary_df, primary_detail)

    if trend_rows:
        lines.append("| " + " | ".join(trend_headers) + " |")
        lines.append("|" + "|".join([":---"] * len(trend_headers)) + "|")
        for row in trend_rows:
            lines.append("| " + " | ".join(row) + " |")
    else:
        lines.append("> 未能提取日度趋势数据，请确认 Excel 中是否包含日期列及对应的日度明细。")
    lines.append("")

    # 三、TOP 排行
    lines.append("## 三、TOP 排行")
    lines.append("")
    top_dim, top_headers, top_rows = None, [], []
    # 优先用 top_sheet（含商品/店铺维度的sheet）生成排行
    if top_df is not None and top_detail:
        top_dim, top_headers, top_rows = build_top_table(top_df, top_detail)
    # 兜底：用明细sheet尝试提取
    elif primary_df is not None and primary_detail:
        top_dim, top_headers, top_rows = build_top_table(primary_df, primary_detail)

    if top_rows:
        lines.append("| " + " | ".join(top_headers) + " |")
        lines.append("|" + "|".join([":---"] * len(top_headers)) + "|")
        for row in top_rows:
            lines.append("| " + " | ".join(row) + " |")
    else:
        lines.append("> 未能提取排行数据，请确认 Excel 中是否包含商品/店铺维度及对应的金额指标。")
    lines.append("")

    # 四、分析总结
    lines.append("## 四、分析总结")
    lines.append("")
    insights = generate_insights(summary_rows, trend_headers, trend_rows, top_dim, top_rows)
    if insights:
        for i, ins in enumerate(insights, 1):
            lines.append(f"{i}. {ins}")
    else:
        lines.append("> 数据不足以自动生成分析总结。建议补充更多指标列（访客数、支付金额、转化率等）。")
    lines.append("")

    # 五、原始数据
    lines.append("## 五、原始数据下载")
    lines.append("")
    lines.append("| 文件 | 路径 |")
    lines.append("|------|------|")
    for path in excel_paths:
        lines.append(f"| {path.name} | `{path}` |")
    lines.append("")

    # 写入文件
    report_text = "\n".join(lines)
    if not output_path:
        safe_name = re.sub(r"[\\/:*?\"<>|]", "_", shop_name)
        output_path = Path("reports") / f"{safe_name}_经营分析_{date_range_str}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")
    print(f"✅ 报告已生成：{output_path}")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="生意参谋 Excel 经营分析报告生成器")
    parser.add_argument("excel", nargs="+", help="生意参谋导出的 Excel 文件路径（支持多个文件合并）")
    parser.add_argument("--shop", help="指定店铺名称（用于报告标题）")
    parser.add_argument("--output", "-o", help="报告输出路径")
    args = parser.parse_args()

    paths = [Path(p) for p in args.excel]
    for p in paths:
        if not p.exists():
            print(f"❌ 文件不存在：{p}", file=sys.stderr)
            return 1

    try:
        output = generate_report(
            paths,
            shop_name=args.shop,
            output_path=Path(args.output) if args.output else None,
        )
        print(output)
    except Exception as e:
        print(f"❌ 生成报告失败：{e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
