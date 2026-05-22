#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""钉钉推送脚本单元测试。"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from dingtalk_send_markdown import ensure_title_has_jingying


class TestEnsureTitle:
    def test_already_has_jingying(self):
        assert ensure_title_has_jingying("上周经营复盘") == "上周经营复盘"

    def test_missing_jingying(self):
        assert ensure_title_has_jingying("上周复盘") == "经营·上周复盘"

    def test_empty(self):
        assert ensure_title_has_jingying("") == "经营分析报告"


class TestMain:
    @patch("os.environ.get", return_value="")
    def test_skip_when_no_webhook(self, _mock):
        import dingtalk_send_markdown as dsm

        with patch("sys.argv", ["dingtalk_send_markdown.py", "--title", "test"]):
            assert dsm.main() == 0

    @patch("os.environ.get", return_value="https://oapi.dingtalk.com/robot/send?access_token=xxx")
    @patch("urllib.request.urlopen")
    def test_successful_push(self, mock_urlopen, _mock_env):
        import dingtalk_send_markdown as dsm

        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"errcode":0,"errmsg":"ok"}'
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        with patch("sys.argv", ["dingtalk_send_markdown.py", "--title", "经营测试", "-f", __file__]):
            assert dsm.main() == 0

    @patch("os.environ.get", return_value="https://oapi.dingtalk.com/robot/send?access_token=xxx")
    @patch("urllib.request.urlopen")
    def test_failed_push(self, mock_urlopen, _mock_env):
        import dingtalk_send_markdown as dsm

        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"errcode":400001,"errmsg":"invalid timestamp"}'
        mock_urlopen.return_value.__enter__.return_value = mock_resp

        with patch("sys.argv", ["dingtalk_send_markdown.py", "--title", "经营测试", "-f", __file__]):
            assert dsm.main() == 1
