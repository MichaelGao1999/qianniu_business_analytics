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
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from constants import BJ_TZ, DATE_FMT, DATETIME_FMT, METRIC_KEYWORDS


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
    priority = [
        "访客数", "浏览量", "支付金额", "支付买家数", "支付转化率", 
        "客单价", "加购人数", "收藏人数", "订单数", "退款金额", "退款率"
    ]
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
    priority = [
        "访客数", "浏览量", "支付金额", "支付买家数", "支付转化率", 
        "客单价", "加购人数", "收藏人数", "订单数", "退款金额", "退款率",
        "手淘搜索访客", "手淘首页访客", "淘内免费访客", "直播访客"
    ]
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

    numeric_cols = numeric_cols[:8]
    headers = ["日期"] + numeric_cols
    rows = []
    for _, row in df.iterrows():
        d = row[date_col]
        date_str = d.strftime(DATE_FMT) if hasattr(d, "strftime") else str(d)[:10]
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

    display_dim = "店铺" if dim_col == "_shop_name" else dim_col
    return display_dim, headers, rows


def generate_insights(
    summary_rows: List[Tuple[str, str]],
    headers: List[str],
    trend_rows: List[List[str]],
    top_dim: Optional[str],
    top_rows: List[List[str]],
    multi_shop: bool = False,
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

    if multi_shop:
        if amount_val:
            insights.append(f"统计周期内 {len(top_rows)} 家店铺支付金额合计达 **{amount_val}**，整体经营规模可观。")
        if visitor_val:
            insights.append(f"全周期访客数合计为 **{visitor_val}**，流量基础稳固。")
    else:
        if amount_val:
            insights.append(f"统计周期内店铺支付金额达 **{amount_val}**，整体经营规模可观。")
        if visitor_val:
            insights.append(f"全周期访客数为 **{visitor_val}**，流量基础稳固。")

    # 多店场景跳过单店首尾对比（trend_rows 含多家店铺，逻辑不适用）
    if not multi_shop and len(trend_rows) >= 2:
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
        insights.append(f"统计周期共覆盖 **{len(trend_rows)} 条日度记录**，可用于进一步做同比/环比分析。")

    if top_rows:
        top_name = top_rows[0][0] if top_rows else ""
        top_val = top_rows[0][1] if top_rows else ""
        if multi_shop:
            insights.append(f"店铺支付金额排行中，**{top_name}** 以 **{top_val}** 位居首位，是核心贡献店铺。")
            if len(top_rows) >= 2:
                last_name = top_rows[-1][0]
                last_val = top_rows[-1][1]
                insights.append(f"尾部店铺 **{last_name}** 支付金额为 **{last_val}**，建议关注增长空间或资源倾斜。")
            if len(top_rows) >= 2:
                try:
                    first_num = float(top_rows[0][1].replace("¥", "").replace(",", ""))
                    last_num = float(top_rows[-1][1].replace("¥", "").replace(",", ""))
                    if last_num > 0:
                        gap = (first_num - last_num) / last_num * 100
                        insights.append(f"头部与尾部店铺支付金额差距约 **{gap:.0f}%**，店铺间经营差异显著，可进一步诊断 Gap 成因。")
                except Exception:
                    pass
        else:
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


def infer_shop_name_from_path(path: Path) -> str:
    """从文件名推断店铺名，如 '测试旗舰店_20260401_20260407.xlsx' -> '测试旗舰店'"""
    fname = path.stem
    m = re.match(r"(.+?)_\d{8}(_\d{8})?", fname)
    return m.group(1) if m else fname


def build_multi_shop_summary(merged_df: pd.DataFrame, info: Dict[str, Any]) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str, str]]]:
    """多店场景：返回 (合计指标, 分店铺汇总表数据)。"""
    metrics = info["metrics"]
    priority = [
        "支付金额", "访客数", "浏览量", "支付买家数", "支付转化率", 
        "客单价", "加购人数", "收藏人数", "订单数", "退款金额", "退款率"
    ]
    total_rows: List[Tuple[str, str]] = []
    for metric in priority:
        col = metrics.get(metric)
        if col and col in merged_df.columns:
            if metric in ["支付转化率", "退款率", "复购率"]:
                val = merged_df[col].mean()
            else:
                val = merged_df[col].sum()
            total_rows.append((metric, smart_fmt(col, val)))

    shop_col = "_shop_name"
    shop_rows: List[Tuple[str, str, str]] = []
    if shop_col in merged_df.columns:
        amount_col = metrics.get("支付金额")
        visitor_col = metrics.get("访客数")
        group_cols = [c for c in [amount_col, visitor_col] if c and c in merged_df.columns]
        if amount_col and group_cols:
            grouped = merged_df.groupby(shop_col)[group_cols].sum().reset_index()
            grouped = grouped.sort_values(by=amount_col, ascending=False)
            for _, row in grouped.iterrows():
                shop_name_val = str(row[shop_col])[:20]
                amount_val = smart_fmt(amount_col, row[amount_col])
                visitor_val = smart_fmt(visitor_col, row[visitor_col]) if visitor_col and visitor_col in row else "-"
                shop_rows.append((shop_name_val, amount_val, visitor_val))
    return total_rows, shop_rows


def build_multi_shop_trend(df: pd.DataFrame, info: Dict[str, Any]) -> Tuple[List[str], List[List[str]]]:
    """多店场景：日度趋势按日期×店铺展示。"""
    date_col = info["date_col"]
    shop_col = "_shop_name"
    if not date_col or shop_col not in df.columns:
        return [], []

    df = df.copy()
    df[date_col] = parse_date_column(df[date_col])
    df = df.dropna(subset=[date_col])

    metrics = info["metrics"]
    amount_col = metrics.get("支付金额")
    visitor_col = metrics.get("访客数")
    numeric_cols = [c for c in [amount_col, visitor_col] if c and c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
    if not numeric_cols:
        return [], []

    grouped = df[[date_col, shop_col] + numeric_cols].groupby([date_col, shop_col]).sum().reset_index()
    headers = ["日期", "店铺"] + numeric_cols
    rows = []
    for _, row in grouped.iterrows():
        d = row[date_col]
        date_str = d.strftime(DATE_FMT) if hasattr(d, "strftime") else str(d)[:10]
        vals = [smart_fmt(col, row[col]) for col in numeric_cols]
        rows.append([date_str, str(row[shop_col])[:20]] + vals)
    return headers, rows


def generate_report(excel_paths: List[Path], shop_name: Optional[str] = None, output_path: Optional[Path] = None) -> Path:
    """生成四段式 Markdown 经营分析报告（支持单店/多店）。"""
    if not excel_paths:
        raise ValueError("未提供 Excel 文件")

    # 读取并分析所有 Excel
    all_sheets = {}
    all_analysis = []
    shop_names = []
    for path in excel_paths:
        sheets = read_excel_file(path)
        all_sheets[str(path)] = sheets
        all_analysis.append(analyze_sheets(sheets))
        shop_names.append(infer_shop_name_from_path(path))

    is_multi_shop = len(excel_paths) > 1

    primary_sheets = list(all_sheets.values())[0]
    primary_analysis = all_analysis[0]
    primary_detail = primary_analysis["detail_sheet"]
    primary_df = primary_sheets[primary_detail["name"]] if primary_detail else None
    top_detail = primary_analysis["top_sheet"]
    top_df = primary_sheets[top_detail["name"]] if top_detail else None

    # 多店合并：将所有 detail_sheet 合并，添加 _shop_name 列
    if is_multi_shop:
        merged_frames = []
        for i, path in enumerate(excel_paths):
            sheets = all_sheets[str(path)]
            analysis = all_analysis[i]
            detail = analysis["detail_sheet"]
            if detail:
                df = sheets[detail["name"]].copy()
                df["_shop_name"] = shop_names[i]
                merged_frames.append(df)
        if merged_frames:
            merged_df = pd.concat(merged_frames, ignore_index=True)
            merged_detail = {
                "name": "merged",
                "shape": merged_df.shape,
                "columns": list(merged_df.columns),
                "date_col": primary_detail["date_col"] if primary_detail else None,
                "shop_col": "_shop_name",
                "item_col": None,
                "metrics": primary_detail["metrics"] if primary_detail else {},
            }
            primary_df = merged_df
            primary_detail = merged_detail
            top_df = merged_df
            top_detail = merged_detail

    # 推断报告标题
    if not shop_name:
        shop_name = "淘系多店" if is_multi_shop else shop_names[0]

    # 推断日期范围
    date_range_str = ""
    if primary_df is not None and primary_detail and primary_detail["date_col"]:
        date_col = primary_detail["date_col"]
        dates = parse_date_column(primary_df[date_col]).dropna()
        if len(dates) > 0:
            date_range_str = f"{dates.min().strftime('%Y%m%d')}_{dates.max().strftime('%Y%m%d')}"
    if not date_range_str:
        date_range_str = datetime.now(BJ_TZ).strftime(DATE_FMT_COMPACT)

    # 构建报告
    lines = []
    lines.append(f"# {shop_name} 经营分析报告")
    lines.append("")
    lines.append(f"> 统计周期：{date_range_str.replace('_', ' 至 ')} ｜ 数据来源：生意参谋导出Excel ｜ 生成时间：{datetime.now(BJ_TZ).strftime(DATETIME_FMT)}")

    lines.append("")

    # 一、整体指标
    lines.append("## 一、整体指标")
    lines.append("")
    summary_rows = []
    shop_summary_rows = []
    if primary_df is not None and primary_detail:
        if is_multi_shop and "_shop_name" in primary_df.columns:
            summary_rows, shop_summary_rows = build_multi_shop_summary(primary_df, primary_detail)
        else:
            summary_rows = build_summary_table(primary_df, primary_detail)

    if summary_rows:
        lines.append("| 指标 | 数值 |")
        lines.append("|------|------|")
        for label, val in summary_rows:
            lines.append(f"| {label} | {val} |")
    else:
        lines.append("> 未能自动识别汇总指标，请检查 Excel 列名是否包含常见指标（如访客数、支付金额、转化率等）。")

    # 多店分店铺汇总小表
    if is_multi_shop and shop_summary_rows:
        lines.append("")
        lines.append("**分店铺汇总**")
        lines.append("")
        lines.append("| 店铺 | 支付金额 | 访客数 |")
        lines.append("|------|----------|--------|")
        for sname, amount, visitor in shop_summary_rows:
            lines.append(f"| {sname} | {amount} | {visitor} |")
    lines.append("")

    # 二、日度趋势
    lines.append("## 二、日度趋势")
    lines.append("")
    trend_headers, trend_rows = [], []
    if primary_df is not None and primary_detail:
        if is_multi_shop and "_shop_name" in primary_df.columns:
            trend_headers, trend_rows = build_multi_shop_trend(primary_df, primary_detail)
        else:
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
    if top_df is not None and top_detail:
        top_dim, top_headers, top_rows = build_top_table(top_df, top_detail)
    elif primary_df is not None and primary_detail:
        top_dim, top_headers, top_rows = build_top_table(primary_df, primary_detail)

    if top_rows:
        # 多店内部列名替换为友好名称
        display_headers = [h if h != "_shop_name" else "店铺" for h in top_headers]
        lines.append("| " + " | ".join(display_headers) + " |")
        lines.append("|" + "|".join([":---"] * len(display_headers)) + "|")
        for row in top_rows:
            lines.append("| " + " | ".join(row) + " |")
    else:
        lines.append("> 未能提取排行数据，请确认 Excel 中是否包含商品/店铺维度及对应的金额指标。")
    lines.append("")

    # 四、分析总结
    lines.append("## 四、分析总结")
    lines.append("")
    insights = generate_insights(summary_rows, trend_headers, trend_rows, top_dim, top_rows, is_multi_shop)
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
