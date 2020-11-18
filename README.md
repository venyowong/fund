# fund
个人平时使用到的基金工具

help
----
```
>python main.py -h
usage: main.py [-h] --target TARGET [--fundcode FUNDCODE] [--outformat OUTFORMAT] [--output OUTPUT] [--user_asset_csv USER_ASSET_CSV]

optional arguments:
  -h, --help            show this help message and exit
  --target TARGET       命令：get_nav, get_asset_config, analyze_asset_allocation, get_date_effect_strategy
  --fundcode FUNDCODE
  --outformat OUTFORMAT
                        输出格式
  --output OUTPUT       输出目录
  --user_asset_csv USER_ASSET_CSV
                        用户资产明细文件
```
get_nav
-------

python main.py --target get_nav --fundcode 502023

获取基金所有历史净值

get_asset_config
----------------

python main.py --target get_asset_config --fundcode 502023

获取基金的持仓配置

get_date_effect_strategy
------------------------

python main.py --target get_date_effect_strategy

获取日历效应策略组合基金

根据天风证券研究表明，基金业绩在每年三月末具有较好的持续性，因此推荐在每年三月末测试日历效应策略
