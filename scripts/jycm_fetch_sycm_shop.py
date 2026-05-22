#!/usr/bin/env python3
"""
【已归档】淘系生意参谋店铺经营数据取数脚本

状态：本脚本为早期 API 取数实现，BASE_URL 为占位地址（api.example.com），
      当前项目主力数据流为「本地 Excel 驱动」（见 jycm_auto_report.py）。
      在接入真实 API 环境前，禁止直接运行本脚本。

范围：仅淘系（天猫淘宝 → 生意参谋），不支持京东 / 抖音 / 全渠道。
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta

from constants import BJ_TZ, DATE_FMT, ISO8601_BJ_START

BASE_URL = "https://api.example.com"

def get_env_token():
    """从环境变量获取 cookie"""
    cookie = os.environ.get("PLATFORM_COOKIE")
    if not cookie:
        raise ValueError("PLATFORM_COOKIE environment variable not set")
    return cookie

def fetch_with_session(endpoint, method="GET", params=None, json_data=None, cookie=None):
    """带 cookie 的请求"""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Cookie": cookie,
        "Content-Type": "application/json"
    }

    if method == "GET":
        resp = requests.get(url, params=params, headers=headers)
    else:
        resp = requests.post(url, json=json_data, headers=headers)

    resp.raise_for_status()
    return resp.json()

def get_channel_list(cookie):
    """获取渠道列表"""
    return fetch_with_session("/fetchData/getChannelList.json", cookie=cookie)

def get_data_platform_map(channel_name, cookie):
    """获取数据平台列表"""
    return fetch_with_session(
        "/fetchData/getDataPlatformMap.json",
        params={"channelName": channel_name},
        cookie=cookie
    )

def get_data_type_map(channel_name, data_platform, cookie):
    """获取数据类型映射"""
    return fetch_with_session(
        "/fetchData/getDataTypeMapList.json",
        params={"channelName": channel_name, "dataPlatform": data_platform},
        cookie=cookie
    )

def get_data_dimension_map(channel_name, data_platform, data_type, cookie):
    """获取数据维度映射"""
    return fetch_with_session(
        "/fetchData/getDataDimensionMapList.json",
        params={"channelName": channel_name, "dataPlatform": data_platform, "dataType": data_type},
        cookie=cookie
    )

def get_date_type_list(channel_name, data_platform, data_type, data_dimension, cookie):
    """获取日期类型列表"""
    return fetch_with_session(
        "/fetchData/getDateTypeList.json",
        params={
            "channelName": channel_name,
            "dataPlatform": data_platform,
            "dataType": data_type,
            "dataDimension": data_dimension
        },
        cookie=cookie
    )

def get_indicators(channel_name, data_platform, data_type, data_dimension, date_type, cookie):
    """获取指标列表"""
    return fetch_with_session(
        "/fetchData/getIndicatorListByDims.json",
        method="POST",
        json_data={
            "channelName": channel_name,
            "dataPlatform": data_platform,
            "dataType": data_type,
            "dataDimension": data_dimension,
            "dateType": date_type
        },
        cookie=cookie
    )

def get_all_shop_list(cookie):
    """获取所有店铺列表"""
    return fetch_with_session("/fetchData/getAllShopList.json", cookie=cookie)

def create_and_download(report_config, cookie):
    """创建并下载报表"""
    return fetch_with_session(
        "/fetchData/createAndDownload.json",
        method="POST",
        json_data=report_config,
        cookie=cookie
    )

def get_shop_list_by_channel(channel_name, cookie):
    """为指定渠道获取店铺列表（本技能固定传入 `天猫淘宝`）"""
    # 获取所有绑定店铺后按渠道过滤，留下淘系店铺
    shop_resp = get_all_shop_list(cookie)
    shops = shop_resp.get('data', [])
    # 过滤指定渠道的店铺
    filtered_shops = [s for s in shops if s.get('channelName') == channel_name]
    if filtered_shops:
        return filtered_shops
    return shops  # 如果没有匹配的，返回全部

def fetch_single_platform_report(channel_name, data_platform, data_type, data_dimension, start_date, end_date, cookie):
    """获取单个平台的报表"""
    print(f"\n{'='*50}")
    print(f"获取平台: {channel_name} - {data_platform}")
    print(f"{'='*50}")

    # Step A: 获取渠道列表（验证）
    print("\n[步骤 A] 获取渠道列表...")
    channel_resp = get_channel_list(cookie)
    print(f"渠道列表: {channel_resp.get('data', [])}")

    # Step B: 获取数据平台映射
    print("\n[步骤 B] 获取数据平台映射...")
    platform_resp = get_data_platform_map(channel_name, cookie)
    platforms = platform_resp.get('data', [])
    print(f"可用平台: {[(p['type'], p['platform']) for p in platforms]}")

    # Step C: 获取数据类型映射
    print("\n[步骤 C] 获取数据类型映射...")
    data_type_resp = get_data_type_map(channel_name, data_platform, cookie)
    print(f"数据类型: {list(data_type_resp.get('data', {}).keys())}")

    # Step D: 获取数据维度映射
    print("\n[步骤 D] 获取数据维度映射...")
    dim_resp = get_data_dimension_map(channel_name, data_platform, data_type, cookie)
    print(f"数据维度: {list(dim_resp.get('data', {}).keys())}")

    # Step E: 获取日期类型
    print("\n[步骤 E] 获取日期类型...")
    date_type_resp = get_date_type_list(channel_name, data_platform, data_type, data_dimension, cookie)
    print(f"日期类型: {date_type_resp.get('data', [])}")

    # Step F: 获取指标列表
    print("\n[步骤 F] 获取指标列表...")
    indicator_resp = get_indicators(channel_name, data_platform, data_type, data_dimension, "day", cookie)
    indicators = list(indicator_resp.get('data', {}).keys())
    print(f"指标数量: {len(indicators)}")

    # Step S: 获取店铺列表
    print("\n[步骤 S] 获取店铺列表...")
    shop_resp = get_all_shop_list(cookie)
    shops = shop_resp.get('data', [])
    shop_ids = [str(s['id']) for s in shops]
    print(f"店铺总数: {len(shops)}")

    # Step G: 创建并下载报表
    print("\n[步骤 G] 创建并下载报表...")
    report_config = {
        "id": 0,
        "reportName": f"{data_platform}{data_type}{data_dimension}上周销售分析",
        "datasource": "电商后台",
        "channelName": channel_name,
        "dataPlatform": data_platform,
        "dataType": data_type,
        "dataDimension": data_dimension,
        "dateType": "day",
        "startDate": start_date,
        "endDate": end_date,
        "shopIds": shop_ids,
        "indicators": indicators,
        "isAutoUpdate": "0",
        "isDataFormat": "Y"
    }

    download_resp = create_and_download(report_config, cookie)

    if download_resp.get('code') == 0 and download_resp.get('success'):
        url = download_resp.get('data', {}).get('url') or download_resp.get('data', {}).get('downloadUrl')
        print(f"\n成功！下载链接: {url}")
        return url
    else:
        print(f"失败: {download_resp}")
        return None

def main():
    # 命令行参数支持自定义时间
    # python3 jycm_fetch_sycm_shop.py [channel] [start_date] [end_date]
    # 日期格式: YYYY-MM-DD
    raise NotImplementedError("本脚本已归档，当前请使用 jycm_auto_report.py（Excel 驱动流）。")
    cookie = get_env_token()  # noqa: F841
    channel_name = sys.argv[1] if len(sys.argv) > 1 else "天猫淘宝"
    data_platform = sys.argv[2] if len(sys.argv) > 2 else "生意参谋"
    start_date_str = sys.argv[3] if len(sys.argv) > 3 else None
    end_date_str = sys.argv[4] if len(sys.argv) > 4 else None

    # 默认时间范围：上周（自然周，上周一到上周日）
    today = datetime.now(BJ_TZ).date()
    days_since_monday = today.weekday()  # 0=Monday
    last_monday = today - timedelta(days=days_since_monday + 7)
    last_sunday = last_monday + timedelta(days=6)

    # 注意：后端按 ISO8601 解析日期，**时区必须显式写成北京时区 +08:00、时间部分统一为 T00:00:00+08:00**（即结束日当天的零点）；
    # 禁用 `T23:59:59.999+08:00`：后端实测会多返回次日数据（如 4/20-4/26 会拿到 4/27），导致区间多一天；
    # 禁用 `Z`（UTC）：`23:59:59Z` 会被解释为次日 07:59:59（北京时间），同样导致区间多一天。
    if start_date_str and end_date_str:
        start_date = start_date_str + ISO8601_BJ_START
        end_date = end_date_str + ISO8601_BJ_START
        last_monday = datetime.strptime(start_date_str, DATE_FMT).date()
        last_sunday = datetime.strptime(end_date_str, DATE_FMT).date()
    else:
        start_date = last_monday.strftime(DATE_FMT) + ISO8601_BJ_START
        end_date = last_sunday.strftime(DATE_FMT) + ISO8601_BJ_START

    print(f"时间范围: {last_monday} 至 {last_sunday}")
    print(f"开始日期: {start_date}")
    print(f"结束日期: {end_date}")

    # 获取单个平台的报表
    result = fetch_single_platform_report(
        channel_name,
        data_platform,
        "店铺",
        "整体",
        start_date,
        end_date,
        cookie
    )

    print(f"\n最终下载链接: {result}")

if __name__ == "__main__":
    main()
