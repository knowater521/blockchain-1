"""区块的数据结构"""

"""
dict类型：
{
    "index": 0,                         # 索引
    "pre_hash": "j35jktj3i4tnf34itj3",  # 前一个区块的hash
    "timestap": 36454545.35435,         # 时间戳
    "randnum": 34.35435,                # 使区块满足某种条件的随机数
    "transactions": [                   # 最多10条交易
        ...
    ]           # 第一条交易包含新区块的交易和其它交易的所有交易费
}
"""

class Block:
    pass