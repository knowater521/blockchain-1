"""区块的数据结构"""

"""
dict类型：
{
    "index": 0,                         # 索引
    "pre_hash": "j35jktj3i4tnf34itj3",  # 前一个区块的hash
    "timestap": 36454545.35435,         # 时间戳
    "randnum": 34.35435,                # 使区块满足某种条件的随机数
    "transactions": [                   # 交易数量有上限
        ...
    ]           # 第一条交易包含新区块的交易和其它交易的所有交易费
}
"""
import json
from time import time
from typing import Any, List

from .transaction import Transaction

class Block:
    """管理区块的类"""
    def __init__(self, index: int=0, pre_hash: str="0"*64) -> None:
        """初始化"""
        self.index = index          # 索引
        self.pre_hash = pre_hash    # 前一个区块的hash
        self.timestap = time()      # 时间戳
        self.randnum = 0.0          # 随机数
        self.transactions = []      # 交易
    
    def add_transaction(self, trans: Transaction) -> None:
        """添加交易"""
        self.transactions.append(trans)

    def keys(self) -> List[str]:
        return [
            "index",
            "pre_hash",
            "timestap",
            "randnum",
            "transactions"
        ]

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __str__(self) -> str:
        return json.dumps(dict(self)).replace(" ", "")

