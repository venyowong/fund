# 基金基础信息相关

from bs4 import BeautifulSoup as bs
import requests
import re


def parse_rate(rate):
    if rate is None:
        return 0
    if rate.find("%") < 0:
        return 0
    return float(rate.strip('%'))


def get_asset_config(fundcode):
    """获取基金资产配置"""
    if fundcode is None:
        print("fundcode is None")
        return None

    try:
        html = requests.get("http://fundf10.eastmoney.com/zcpz_{}.html".format(fundcode)).content
        soup = bs(html, 'html.parser')
        tds = soup.select_one("table.w782.comm.tzxq>tbody>tr").select("td")
        return {"stock": parse_rate(tds[1].text), "bond": parse_rate(tds[2].text),
                "cash": parse_rate(tds[3].text)}
    except BaseException as error:
        print("caught an exception in get_asset_config for {}".format(fundcode))
        print(error)


def get_fund_scale(fundcode):
    """获取基金规模"""
    if fundcode is None:
        print("fundcode is None")
        return None

    try:
        html = requests.get("http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=gmbd&code={}"
                            .format(fundcode)).text
        soup = bs(re.search(r"<table[^\"]*</table>", html).group(), 'html.parser')
        tds = soup.select_one("table.w782.comm.gmbd>tbody>tr").select("td")
        return {"end_asset": float(tds[4].text)}
    except BaseException as error:
        print("caught an exception in get_asset_config for {}".format(fundcode))
        print(error)
