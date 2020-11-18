# 基金净值相关

import requests
import json
import pandas as pd


def get_nav(fundcode):
    """获取基金净值"""
    if fundcode is None:
        print("fundcode is None")
        return None

    try:
        response = requests.get("http://api.fund.eastmoney.com/f10/lsjz?fundCode={}&pageIndex=1&pageSize=10000"
                     .format(fundcode), headers={"Referer": "http://fundf10.eastmoney.com/jjjz_{}.html".format(fundcode)})
        result = json.loads(response.text)
        navs = []
        for item in result["Data"]["LSJZList"]:
            navs.append([item["FSRQ"], item["LJJZ"], item["DWJZ"]])
        return pd.DataFrame(navs, columns=["date", "acc_unit_nav", "unit_nav"])
    except BaseException as error:
        print("caught an exception in get_nav for {}".format(fundcode))
        print(error)
