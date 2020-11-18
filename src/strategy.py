# 基金策略相关
import requests
import re
import json
import pandas as pd
import numpy as np
import fund

def get_fund_rank_info(string):
    """将逗号分隔的数据解析成排行对象"""
    if string is None:
        return None

    strs = string.split(",")
    result = {"fundcode": strs[0], "fundname": strs[1], "date": strs[3], "nav_grow_1y": float(strs[11])}
    return result


def get_fund_ranking(fundtype):
    """获取基金排行
    http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=hh&gs=0&sc=1nzf&st=desc&sd=2019-11-12&ed=2020-11-18&pi=1&pn=50&dx=0
    ft：hh 混合 gp 股票 qdii  sc：1nzf 一年涨幅  sd：起始日期  ed：截止日期  pn：数量  dx：0 全部 1 可购"""
    url = "http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft={}&gs=0&sc=1nzf&st=desc&pi=1&pn=100&dx=0"\
        .format(fundtype)
    response = requests.get(url, headers={"Referer": "http://fund.eastmoney.com/data/fundranking.html"})
    rl = json.loads(re.search(r"\[[^\]]*\]", response.text).group())
    return list(map(lambda x: get_fund_rank_info(x), rl))


def deextremum(x, median, sigma, max_, min_):
    """去极值"""
    l1 = median - 3.5 * sigma
    l2 = median - 3 * sigma
    r1 = median + 3.5 * sigma
    r2 = median + 3 * sigma
    if l2 <= x <= r2:
        return x

    if x < l2:
        return l2 - (l2 - x) / (l2 - min_) * (l2 - l1)

    return r2 + (x - r2) / (max_ - r2) * (r1 - r2)


def get_date_effect_strategy():
    """日历效应策略"""
    print("""根据天风证券研究表明，基金业绩在每年三月末具有较好的持续性，因此推荐在每年三月末测试日历效应策略""")
    funds = get_fund_ranking("gp")
    funds.extend(get_fund_ranking("hh"))
    funds.extend(get_fund_ranking("qdii"))
    funds = [f for f in funds if f["fundname"][-1] not in ["B", "C", "E", "H", "O"]]
    df = pd.DataFrame(funds)
    median = np.median(df["nav_grow_1y"])  # 中位数
    mad = np.median(df["nav_grow_1y"].apply(lambda x: np.abs(x - median)))  # 绝对中位数
    sigma = 1.4826 * mad
    max_ = df["nav_grow_1y"].max()
    min_ = df["nav_grow_1y"].min()
    df["factor"] = df["nav_grow_1y"].apply(deextremum, args=(median, sigma, max_, min_))
    mean = np.mean(df["factor"])
    std = np.std(df["factor"])
    df["factor"] = df["factor"].apply(lambda x: (x - mean) / std)  # 标准化
    df = df.nlargest(10, "factor")
    funds = []
    for i in range(len(df)):
        item = df.iloc[i]
        if fund.get_fund_scale(item["fundcode"])["end_asset"] >= 2:
            funds.append(item)
    return pd.DataFrame(funds).nlargest(5, "factor")
