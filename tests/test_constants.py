#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""常量定义验证。"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from constants import (
    BJ_TZ,
    DATE_FMT,
    DATETIME_FMT,
    ISO8601_BJ_START,
    MAX_TEXT_DINGTALK,
    MAX_TEXT_FEISHU,
    METRIC_KEYWORDS,
)


def test_bj_tz_is_plus_8():
    assert BJ_TZ.utcoffset(None).total_seconds() == 8 * 3600


def test_date_fmt_is_iso():
    assert DATE_FMT == "%Y-%m-%d"
    assert DATETIME_FMT == "%Y-%m-%d %H:%M"


def test_iso8601_bj_start():
    assert "T00:00:00+08:00" in ISO8601_BJ_START


def test_max_text_positive():
    assert MAX_TEXT_DINGTALK > 0
    assert MAX_TEXT_FEISHU > 0
    assert MAX_TEXT_DINGTALK > MAX_TEXT_FEISHU


def test_metric_keywords_not_empty():
    assert "支付金额" in METRIC_KEYWORDS
    assert "访客数" in METRIC_KEYWORDS
    assert len(METRIC_KEYWORDS) > 0
