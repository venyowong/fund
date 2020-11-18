import sys
import nav
import argparse
import pandas as pd
import fund
import asset
import strategy

def output(args, data):
    """输出 DataFrame"""
    if data is None or args is None:
        return

    if data is pd.DataFrame and args.outformat == "csv":
        if args.output is None:
            data.to_csv("{}.csv".format(args.fundcode))
        else:
            data.to_csv("{0}{1}.csv".format(args.output, args.fundcode))
    else:
        print(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="命令：get_nav, get_asset_config, analyze_asset_allocation, "
                                                        "get_date_effect_strategy")
    parser.add_argument("--fundcode", required=False)
    parser.add_argument("--outformat", required=False, help="输出格式")
    parser.add_argument("--output", required=False, help="输出目录")
    parser.add_argument("--user_asset_csv", required=False, help="用户资产明细文件")
    args = parser.parse_args()
    if args.target == "get_nav":
        output(args, nav.get_nav(args.fundcode))
    if args.target == "get_asset_config":
        output(args, fund.get_asset_config(args.fundcode))
    if args.target == "analyze_asset_allocation":
        output(args, asset.analyze_asset_allocation(args.user_asset_csv))
    if args.target == "get_date_effect_strategy":
        output(args, strategy.get_date_effect_strategy())
    else:
        parser.print_help()
