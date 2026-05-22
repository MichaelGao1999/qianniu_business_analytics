#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生意参谋经营报告自动化脚本（本地Excel驱动 + 飞书推送）

自动完成：扫描 data/ 目录 Excel → 生成 Markdown 分析报告 →（可选）推送到飞书

范围：仅处理淘系（天猫淘宝 → 生意参谋）导出的Excel，不支持京东/抖音/全渠道。
多店支持：同为淘系的多家店铺可将多个Excel放入 data/，合并为一份报告。

用法:
  # 默认扫描 data/ 目录下所有 Excel 并生成报告
  python3 scripts/jycm_auto_report.py

  # 指定店铺名称 + 飞书推送
  python3 scripts/jycm_auto_report.py --shop "XX旗舰店" --feishu

  # 指定具体Excel文件
  python3 scripts/jycm_auto_report.py data/店铺A.xlsx data/店铺B.xlsx --shop "多店合并" --feishu

  # 自定义输出路径
  python3 scripts/jycm_auto_report.py --output reports/自定义报告.md

环境变量:
  export FEISHU_WEBHOOK='https://open.feishu.cn/open-apis/bot/v2/hook/...'
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

from constants import BJ_TZ

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# 允许直接 import 同目录下的分析模块
sys.path.insert(0, str(SCRIPT_DIR))
import analyze_excel_report


def scan_excel_files(data_dir: Path) -> list[Path]:
    """扫描 data/ 目录下所有 Excel 文件。"""
    if not data_dir.exists():
        print(f"⚠️  data/ 目录不存在：{data_dir}，已自动创建")
        data_dir.mkdir(parents=True, exist_ok=True)
        return []

    exts = {".xlsx", ".xls", ".xlsm"}
    files = sorted([f for f in data_dir.iterdir() if f.is_file() and f.suffix.lower() in exts])
    return files


def run_analysis(excel_paths: list[Path], shop_name: str | None = None, output_path: Path | None = None) -> Path | None:
    """调用分析模块生成报告（直接 import，避免 subprocess 开销）。"""
    try:
        report_path = analyze_excel_report.generate_report(
            excel_paths=excel_paths,
            shop_name=shop_name,
            output_path=output_path,
        )
        print(f"报告生成成功：{report_path}")
        return report_path
    except Exception as e:
        print(f"报告生成失败：{e}")
        return None


def send_feishu(report_path: Path, title: str) -> bool:
    """推送到飞书（仅在配置了 FEISHU_WEBHOOK 时执行）。"""
    webhook = os.environ.get("FEISHU_WEBHOOK", "").strip()
    if not webhook:
        print("⚠️  未配置 FEISHU_WEBHOOK，跳过飞书推送。可通过 export FEISHU_WEBHOOK='https://open.feishu.cn/open-apis/bot/v2/hook/...' 启用。")
        return False

    feishu_script = SCRIPT_DIR / "feishu_send_markdown.py"
    if not feishu_script.exists():
        print(f"❌ 飞书推送脚本不存在：{feishu_script}")
        return False

    result = subprocess.run(
        [sys.executable, str(feishu_script), "--title", title, "-f", str(report_path)],
        capture_output=True,
        text=True,
        encoding='utf-8',
    )

    if result.returncode == 0:
        print(f"✅ 飞书推送成功：{title}")
        return True
    else:
        print(f"❌ 飞书推送失败：{result.stderr}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="生意参谋经营报告自动化（本地Excel驱动 + 飞书推送）")
    parser.add_argument("excel", nargs="*", help="指定 Excel 文件路径（省略则扫描 data/ 目录）")
    parser.add_argument("--shop", "-s", help="指定店铺名称（用于报告标题）")
    parser.add_argument("--feishu", action="store_true", help="推送到飞书")
    parser.add_argument("--output", "-o", help="报告输出路径")
    parser.add_argument("--data-dir", default=str(PROJECT_ROOT / "data"), help="Excel 数据目录（默认 data/）")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)

    # 确定要分析的 Excel 文件
    if args.excel:
        excel_paths = [Path(p) for p in args.excel]
        for p in excel_paths:
            if not p.exists():
                print(f"❌ 文件不存在：{p}")
                return 1
    else:
        excel_paths = scan_excel_files(data_dir)
        if not excel_paths:
            print(f"⚠️  {data_dir} 目录下未找到 Excel 文件，请将生意参谋导出的 .xlsx 文件放入该目录。")
            return 1
        print(f"📁 扫描到 {len(excel_paths)} 个 Excel 文件：")
        for p in excel_paths:
            print(f"   - {p.name}")

    # 店铺名称
    shop_name = args.shop
    if not shop_name and len(excel_paths) == 1:
        # 从文件名推断
        shop_name = excel_paths[0].stem
    if not shop_name:
        shop_name = "淘系店铺"

    # 日期范围（从文件名或当前时间推断，仅用于报告标题）
    print(f"\n📊 开始生成报告：{shop_name}")

    # 生成报告
    output_path = Path(args.output) if args.output else None
    report_path = run_analysis(excel_paths, shop_name=shop_name, output_path=output_path)
    if not report_path:
        return 1

    # 飞书推送
    if args.feishu:
        title = f"{shop_name} 经营分析报告"
        send_feishu(report_path, title)

    print("\n✅ 自动化流程完成")
    print(f"   - 店铺：{shop_name}")
    print(f"   - Excel 文件数：{len(excel_paths)}")
    print(f"   - 报告路径：{report_path}")
    if args.feishu:
        webhook = os.environ.get("FEISHU_WEBHOOK", "").strip()
        print(f"   - 飞书推送：{'已启用' if webhook else '未配置 FEISHU_WEBHOOK，已跳过'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
