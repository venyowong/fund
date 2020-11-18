# 用户资产相关

import pandas as pd
import fund


def analyze_asset_allocation(csv_file):
    """分析用户资产配置"""
    if csv_file is None:
        print("csv file is None")
        return None

    details = pd.read_csv(csv_file, dtype={"fundcode": str})
    total = 0
    stock = 0
    bond = 0
    cash = 0
    for i in range(len(details)):
        item = details.iloc[i]
        amount = item["amount"]
        total = total + amount
        config = fund.get_asset_config(item["fundcode"])
        if config is None:
            continue

        stock = stock + amount * config["stock"] / 100
        bond = bond + amount * config["bond"] / 100
        cash = cash + amount * config["cash"] / 100
    return {"total": total, "stock": round(stock, 2), "stock_ratio": round(stock / total, 2),
            "bond": round(bond, 2), "bond_ratio": round(bond / total, 2),
            "cash": round(cash, 2), "cash_ratio": round(cash / total, 2)}
