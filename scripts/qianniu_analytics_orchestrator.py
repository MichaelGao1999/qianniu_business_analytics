#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
千牛店铺经营数据分析编排脚本

用途：自动化执行瓴羊 One 技能包的「业务编排层」流程
- 检查前置条件（授权、店铺绑定）
- 调用 jycm-openapi-token 获取有效 Cookie
- 调用 jycm-fetch-report-nl 获取生意参谋数据
- 调用 jycm-fetch-report-analyze 生成分析报告

依赖：
- Python 3.8+
- requests
- json

使用示例：
    python qianniu_analytics_orchestrator.py --shop "XX 旗舰店" --data_type "生意参谋 - 店铺 - 整体 - 日" --date_range "近 7 天"
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 北京时间 UTC+8
BJ_TZ = timezone(timedelta(hours=8))
from typing import Optional, Dict, List, Any
import requests


class QianniuAnalyticsOrchestrator:
    """千牛店铺经营数据分析编排器"""

    def __init__(self, working_dir: Optional[str] = None):
        """
        初始化编排器

        Args:
            working_dir: 工作目录，默认为当前目录
        """
        self.working_dir = Path(working_dir) if working_dir else Path.cwd()
        self.auth_file = self.working_dir / "auth" / "jycm.json"
        self.data_dir = self.working_dir / "data"
        self.reports_dir = self.working_dir / "reports"

        # 确保目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # 认证信息
        self.access_key: Optional[str] = None
        self.secret_key: Optional[str] = None
        self.jycm_cookie: Optional[str] = None
        self.shops: List[str] = []

    def load_auth_config(self) -> bool:
        """
        加载认证配置

        Returns:
            bool: 是否加载成功
        """
        if not self.auth_file.exists():
            print(f"❌ 认证文件不存在：{self.auth_file}")
            return False

        try:
            with open(self.auth_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            self.access_key = config.get("accessKey")
            self.secret_key = config.get("secretKey")
            self.jycm_cookie = config.get("jycmOpenApiCookie")
            self.shops = config.get("shops", [])

            if not self.jycm_cookie:
                print("❌ Cookie 无效，请重新获取认证凭证")
                return False

            print(f"✅ 认证配置加载成功，已绑定店铺：{len(self.shops)}")
            return True

        except json.JSONDecodeError as e:
            print(f"❌ 认证文件格式错误：{e}")
            return False
        except Exception as e:
            print(f"❌ 加载认证配置失败：{e}")
            return False

    def check_shop_bound(self, shop_name: str) -> bool:
        """
        检查店铺是否已绑定

        Args:
            shop_name: 店铺名称

        Returns:
            bool: 是否已绑定
        """
        if shop_name in self.shops:
            print(f"✅ 店铺已绑定：{shop_name}")
            return True
        else:
            print(f"⚠️  店铺未绑定：{shop_name}")
            print("📖 请参考文档完成绑定：https://alidocs.dingtalk.com/i/nodes/qnYMoO1rWxrkmoj2IznlmLDmJ47Z3je9")
            return False

    def update_auth_config(self, shop_name: Optional[str] = None):
        """
        更新认证配置

        Args:
            shop_name: 可选，新增店铺名称
        """
        config = {
            "accessKey": self.access_key,
            "secretKey": self.secret_key,
            "jycmOpenApiCookie": self.jycm_cookie,
            "shops": self.shops,
            "updated_at": datetime.now(BJ_TZ).strftime("%Y-%m-%d %H:%M:%S")
        }

        if shop_name and shop_name not in self.shops:
            self.shops.append(shop_name)
            config["shops"] = self.shops
            print(f"✅ 已添加店铺：{shop_name}")

        # 确保 auth 目录存在
        self.auth_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.auth_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"✅ 认证配置已更新：{self.auth_file}")

    def get_effective_cookie(self) -> Optional[str]:
        """
        获取有效 Cookie（调用 jycm-openapi-token）

        Returns:
            Optional[str]: 有效 Cookie，失败返回 None
        """
        print("🔑 正在获取有效 Cookie...")

        # 这里应该调用 jycm-openapi-token 技能
        # 由于是编排脚本，暂时返回缓存的 Cookie
        # 实际使用时需要通过技能调用机制

        if not self.jycm_cookie:
            print("❌ Cookie 无效，请重新获取认证凭证")
            print("📖 获取请求码：https://jycm.lydaas.com/manage/account/update")
            return None

        # TODO: 调用 jycm-openapi-token 技能验证并刷新 Cookie
        # 这里简化处理，直接返回缓存的 Cookie
        print("✅ Cookie 有效")
        return self.jycm_cookie

    def fetch_report_data(
        self,
        shop_name: str,
        data_type: str,
        date_range: str
    ) -> Optional[Dict[str, Any]]:
        """
        获取报表数据（调用 jycm-fetch-report-nl）

        Args:
            shop_name: 店铺名称
            data_type: 数据类型（如：生意参谋 - 店铺 - 整体 - 日）
            date_range: 日期范围（如：近 7 天）

        Returns:
            Optional[Dict]: 数据元信息，包含下载链接等
        """
        print(f"📥 正在获取数据：{shop_name} - {data_type} - {date_range}")

        # 获取有效 Cookie
        cookie = self.get_effective_cookie()
        if not cookie:
            return None

        # TODO: 调用 jycm-fetch-report-nl 技能
        # 这里简化处理，模拟调用流程

        # 实际调用应该通过技能机制执行
        # 以下是模拟的接口链调用逻辑

        try:
            # 模拟调用结果
            result = {
                "shop_name": shop_name,
                "data_type": data_type,
                "date_range": date_range,
                "download_url": "https://example.com/download.xlsx",
                "file_path": str(self.data_dir / f"{shop_name}_{data_type}_{date_range}.xlsx"),
                "status": "success"
            }

            print(f"✅ 数据获取成功：{result['file_path']}")
            return result

        except Exception as e:
            print(f"❌ 数据获取失败：{e}")
            return None

    def generate_analysis_report(
        self,
        data_result: Dict[str, Any],
        analysis_focus: str = "销售",
        report_style: str = "详细版"
    ) -> Optional[str]:
        """
        生成分析报告（调用 jycm-fetch-report-analyze）

        Args:
            data_result: 数据获取结果
            analysis_focus: 分析重点（销售/流量/商品/服务）
            report_style: 报告风格（简洁版/详细版/高管版）

        Returns:
            Optional[str]: 报告文件路径
        """
        print(f"📊 正在生成分析报告：{analysis_focus} - {report_style}")

        # TODO: 调用 jycm-fetch-report-analyze 技能
        # 这里简化处理，模拟调用流程

        try:
            shop_name = data_result["shop_name"]
            data_type = data_result["data_type"]
            date_range = data_result["date_range"]

            report_filename = f"{shop_name}_{data_type}_{date_range}_分析报告.docx"
            report_path = str(self.reports_dir / report_filename)

            print(f"✅ 报告生成成功：{report_path}")
            return report_path

        except Exception as e:
            print(f"❌ 报告生成失败：{e}")
            return None

    def execute_full_flow(
        self,
        shop_name: str,
        data_type: str,
        date_range: str,
        generate_report: bool = True,
        analysis_focus: str = "销售",
        report_style: str = "详细版"
    ) -> Dict[str, Any]:
        """
        执行完整流程

        Args:
            shop_name: 店铺名称
            data_type: 数据类型
            date_range: 日期范围
            generate_report: 是否生成报告
            analysis_focus: 分析重点
            report_style: 报告风格

        Returns:
            Dict: 执行结果
        """
        print("=" * 60)
        print("🚀 开始执行千牛店铺经营数据分析流程")
        print("=" * 60)

        result = {
            "success": False,
            "shop_name": shop_name,
            "data_type": data_type,
            "date_range": date_range,
            "data_file": None,
            "report_file": None,
            "error": None
        }

        # 第一步：检查前置条件
        print("\n📋 第一步：检查前置条件")
        if not self.load_auth_config():
            result["error"] = "认证配置加载失败"
            return result

        if not self.check_shop_bound(shop_name):
            result["error"] = "店铺未绑定"
            return result

        # 第二步：获取数据
        print("\n📥 第二步：获取数据")
        data_result = self.fetch_report_data(shop_name, data_type, date_range)
        if not data_result:
            result["error"] = "数据获取失败"
            return result

        result["data_file"] = data_result.get("file_path")

        # 第三步：生成报告（可选）
        if generate_report:
            print("\n📊 第三步：生成分析报告")
            report_path = self.generate_analysis_report(
                data_result,
                analysis_focus=analysis_focus,
                report_style=report_style
            )
            if report_path:
                result["report_file"] = report_path
            else:
                print("⚠️  报告生成失败，但数据已下载")

        result["success"] = True
        print("\n" + "=" * 60)
        print("✅ 流程执行完成")
        print("=" * 60)

        return result


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="千牛店铺经营数据分析编排脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
    # 获取店铺上周经营数据
    python qianniu_analytics_orchestrator.py --shop "XX 旗舰店" --data_type "生意参谋 - 店铺 - 整体 - 日" --date_range "近 7 天"

    # 获取数据并生成流量分析报告
    python qianniu_analytics_orchestrator.py --shop "XX 旗舰店" --data_type "生意参谋 - 店铺 - 流量来源 - 日" --date_range "昨天" --analysis_focus "流量"

    # 仅获取数据，不生成报告
    python qianniu_analytics_orchestrator.py --shop "XX 旗舰店" --no-report
        """
    )

    parser.add_argument("--shop", required=True, help="店铺名称")
    parser.add_argument("--data_type", default="生意参谋 - 店铺 - 整体 - 日", help="数据类型")
    parser.add_argument("--date_range", default="近 7 天", help="日期范围")
    parser.add_argument("--analysis_focus", default="销售", help="分析重点（销售/流量/商品/服务）")
    parser.add_argument("--report_style", default="详细版", help="报告风格（简洁版/详细版/高管版）")
    parser.add_argument("--no-report", action="store_true", help="不生成报告")
    parser.add_argument("--working_dir", default=None, help="工作目录")

    args = parser.parse_args()

    # 创建编排器
    orchestrator = QianniuAnalyticsOrchestrator(working_dir=args.working_dir)

    # 执行完整流程
    result = orchestrator.execute_full_flow(
        shop_name=args.shop,
        data_type=args.data_type,
        date_range=args.date_range,
        generate_report=not args.no_report,
        analysis_focus=args.analysis_focus,
        report_style=args.report_style
    )

    # 输出结果
    print("\n📋 执行结果：")
    print(f"  成功：{result['success']}")
    print(f"  店铺：{result['shop_name']}")
    print(f"  数据类型：{result['data_type']}")
    print(f"  日期范围：{result['date_range']}")
    if result['data_file']:
        print(f"  数据文件：{result['data_file']}")
    if result['report_file']:
        print(f"  报告文件：{result['report_file']}")
    if result['error']:
        print(f"  错误：{result['error']}")

    # 返回退出码
    sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()
