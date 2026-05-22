#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""analyze_excel_report.py 核心逻辑单元测试。"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from analyze_excel_report import (
    build_multi_shop_summary,
    build_multi_shop_trend,
    find_column,
    fmt_currency,
    fmt_number,
    fmt_percent,
    generate_insights,
    infer_shop_name_from_path,
    smart_fmt,
)


class TestFindColumn:
    def test_exact_match(self):
        df = pd.DataFrame({"支付金额(元)": [1, 2]})
        assert find_column(df, ["支付金额"]) == "支付金额(元)"

    def test_no_match(self):
        df = pd.DataFrame({"foo": [1, 2]})
        assert find_column(df, ["支付金额"]) is None

    def test_case_insensitive(self):
        df = pd.DataFrame({"GMV": [1, 2]})
        assert find_column(df, ["gmv"]) == "GMV"


class TestFormatting:
    def test_fmt_number_int(self):
        assert fmt_number(12345) == "12,345"

    def test_fmt_number_float(self):
        assert fmt_number(1234.5) == "1,234.50"

    def test_fmt_number_none(self):
        assert fmt_number(None) == "-"

    def test_fmt_currency(self):
        assert fmt_currency(1234.5) == "¥1,234.50"

    def test_fmt_percent_decimal(self):
        assert fmt_percent(0.1234) == "12.34%"

    def test_fmt_percent_integer(self):
        assert fmt_percent(12.34) == "12.34%"

    def test_smart_fmt_by_name(self):
        assert "¥" in smart_fmt("支付金额", 100)
        assert "%" in smart_fmt("转化率", 0.1)
        assert "100" in smart_fmt("访客数", 100)


class TestInferShopName:
    def test_from_filename_with_dates(self):
        assert infer_shop_name_from_path(Path("测试旗舰店_20260401_20260407.xlsx")) == "测试旗舰店"

    def test_from_filename_plain(self):
        assert infer_shop_name_from_path(Path("店铺A.xlsx")) == "店铺A"


class TestMultiShopSummary:
    def test_basic(self):
        df = pd.DataFrame({
            "_shop_name": ["A", "A", "B", "B"],
            "支付金额": [100.0, 200.0, 50.0, 80.0],
            "访客数": [10, 20, 5, 8],
        })
        info = {"metrics": {"支付金额": "支付金额", "访客数": "访客数"}}
        total, shop = build_multi_shop_summary(df, info)
        # A 合计 300，B 合计 130
        assert any("支付金额" in t[0] for t in total)
        assert len(shop) == 2
        assert shop[0][0] == "A"  # 按金额降序

    def test_empty_df(self):
        df = pd.DataFrame({"_shop_name": [], "支付金额": []})
        info = {"metrics": {"支付金额": "支付金额"}}
        total, shop = build_multi_shop_summary(df, info)
        # 空 df 的 sum 为 0，total 会包含 0 值条目；shop 为空因为无分组数据
        assert shop == []


class TestMultiShopTrend:
    def test_basic(self):
        df = pd.DataFrame({
            "_shop_name": ["A", "A", "B"],
            "日期": ["2026-04-01", "2026-04-02", "2026-04-01"],
            "支付金额": [100.0, 200.0, 50.0],
        })
        info = {"date_col": "日期", "metrics": {"支付金额": "支付金额"}}
        headers, rows = build_multi_shop_trend(df, info)
        assert headers == ["日期", "店铺", "支付金额"]
        assert len(rows) == 3

    def test_missing_shop_col(self):
        df = pd.DataFrame({"日期": ["2026-04-01"], "支付金额": [100.0]})
        info = {"date_col": "日期", "metrics": {"支付金额": "支付金额"}}
        headers, rows = build_multi_shop_trend(df, info)
        assert rows == []


class TestGenerateInsights:
    def test_single_shop_basic(self):
        insights = generate_insights(
            [("支付金额", "¥1,000.00"), ("访客数", "500")],
            ["日期", "支付金额"],
            [["2026-04-01", "¥100"], ["2026-04-02", "¥200"]],
            "商品",
            [["商品A", "¥500"]],
        )
        assert len(insights) >= 2
        assert any("支付金额" in i for i in insights)

    def test_multi_shop(self):
        insights = generate_insights(
            [("支付金额", "¥1,000.00")],
            ["店铺", "支付金额"],
            [["A", "¥100"], ["B", "¥200"]],
            "店铺",
            [["A", "¥600"], ["B", "¥400"]],
            multi_shop=True,
        )
        assert any("店铺支付金额排行" in i for i in insights)
        assert any("尾部店铺" in i for i in insights)

    def test_no_data(self):
        insights = generate_insights([], [], [], None, [])
        assert insights == []
