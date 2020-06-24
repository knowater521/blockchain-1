"""区块的数据结构"""
"""
dict类型：
{
    "index": 0,                         # 索引
    "pre_hash": "j35jktj3i4tnf34itj3",  # 前一个区块的hash
    "timestap": 36454545.35435,         # 时间戳
    "randnum": 34.35435,                # 使区块满足某种条件的随机数
    "transactions": [                   # 交易数量有上限，每个交易都保存为一个字符串
        ...
    ]           # 第一条交易包含新区块的交易和其它交易的所有交易费
}
"""
import json
from hashlib import sha256
from time import time
from typing import Any, List

from config import HEAD_HASH, MINING_ADD_NUM
from .trans_input import TransInput
from .trans_output import TransOutput
from .transaction import Transaction

class Block:
    """管理区块的类"""
    def __init__(self, index: int=0, pre_hash: str="0"*64, block: str="") -> None:
        """初始化"""
        self.index = index          # 索引
        self.pre_hash = pre_hash    # 前一个区块的hash
        self.timestap = time()      # 时间戳
        self.randnum = 0.0          # 随机数
        self.transactions: List[Transaction] = []      # 交易
        if block:
            self.load_block(block)
    
    def load_block(self, block: str) -> None:
        """根据json数据导入区块"""
        block_dict = json.loads(block)
        self.index = block_dict.get("index", self.index)        
        self.pre_hash = block_dict.get("pre_hash", self.pre_hash)
        self.timestap = block_dict.get("timestap", self.timestap)
        self.randnum = block_dict.get("randnum", self.randnum)
        trans_list = block_dict.get("transactions", [])    
        if trans_list:
            self.transactions = []
            for trans in trans_list:
                t = Transaction(trans=trans)
                self.add_transaction(t)

    def get_transactions(self) -> List[Transaction]:
        """获取全部交易"""
        return self.transactions

    def get_transaction(self, trans: int) -> Transaction:
        """获取第trans个交易"""
        return self.transactions[trans]

    def get_input(self, trans: int, inp: int) -> TransInput:
        """获取第trans笔交易、inp个输入"""
        return self.get_transaction(trans).get_input(inp)
    
    def get_output(self, trans: int, outp: int) -> TransOutput:
        """获取第trans笔交易、outp个输出"""
        return self.get_transaction(trans).get_output(outp)

    def add_transaction(self, trans: Transaction) -> None:
        """添加交易"""
        self.transactions.append(trans)

    def get_hash(self) -> str:
        """获取本区块的hash值"""
        tap = str(self).encode("utf-8")
        return sha256(tap).hexdigest()

    def veri_hash(self) -> bool:
        """验证区块hash值的合法性"""
        return self.get_hash().startswith(HEAD_HASH)

    def find_randnum(self) -> None:
        """寻找randnum，设定timestap"""
        while not self.veri_hash():
            self.randnum += MINING_ADD_NUM
            self.timestap = time()

    def keys(self) -> List[str]:
        return [
            "index",
            "pre_hash",
            "timestap",
            "randnum",
            "transactions"
        ]

    def __getitem__(self, key: str) -> Any:
        value = getattr(self, key)
        if key == "transactions":   # 每个transaction转换成字符串
            value = [str(tap) for tap in value]
        return value

    def __str__(self) -> str:
        return json.dumps(dict(self)).replace(" ", "")


if __name__ == "__main__":
    from .trans_input import TransInput
    from .trans_output import TransOutput
    trans = Transaction()
    trans.add_input(TransInput(3, 5, 7))
    trans.add_output(TransOutput(5.67, "fsfwetewtette4654654"))
    from key import UserKey
    key = UserKey()
    trans.sign_transaction(key)
    trans2 = Transaction(str(trans))
    trans2.add_input(TransInput(5, 6, 2))
    block = Block()
    block.add_transaction(trans)
    block.add_transaction(trans2)
    tap = str(block)
    print(tap)
    block2 = Block(block=tap)
    print(str(block2))
    print(str(block2) == str(block))
    block.find_randnum()
    print(block.get_hash())
