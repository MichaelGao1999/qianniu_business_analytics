#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jycm_auto_report.py 单元测试。"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from jycm_auto_report import scan_excel_files


class TestScanExcelFiles:
    def test_scan_empty_dir(self):
        with tempfile.TemporaryDirectory() as td:
            result = scan_excel_files(Path(td))
            assert result == []

    def test_scan_mixed_files(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "店铺A.xlsx").write_text("fake")
            (p / "店铺B.xls").write_text("fake")
            (p / "readme.txt").write_text("fake")
            result = scan_excel_files(p)
            assert len(result) == 2
            assert all(f.suffix in {".xlsx", ".xls"} for f in result)

    def test_auto_create_dir(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "nonexistent" / "data"
            result = scan_excel_files(p)
            assert result == []
            assert p.exists()
