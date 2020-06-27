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
import time
from hashlib import sha256
from typing import Any, List

from config import HEAD_HASH, MINING_ADD_NUM, FIREST_BLOCK_PREHASH, MINING_BTCS, REDUCE_BTCS_HEIGHT
from .btc import Btc
from .trans_input import TransInput
from .trans_output import TransOutput
from .transaction import Transaction


__all__ = ["Block", ]


class Block:
    """管理区块的类"""
    def __init__(self, index: int=0, pre_hash: str=FIREST_BLOCK_PREHASH) -> None:
        """初始化"""
        self.index = index          # 索引
        self.pre_hash = pre_hash    # 前一个区块的hash
        self.timestap = time.time() # 时间戳
        self.randnum = 0.0          # 随机数
        self.transactions: List[Transaction] = []       # 交易
        self.head_trans = Transaction()                 # 第一笔交易（矿工奖励和交易费）
    
    @classmethod
    def load_block(cls, block: str) -> "Block":
        """根据json数据导入区块"""
        result = cls()
        block_dict = json.loads(block)
        result.index = block_dict.get("index", result.index)        
        result.pre_hash = block_dict.get("pre_hash", result.pre_hash)
        result.timestap = block_dict.get("timestap", result.timestap)
        result.randnum = block_dict.get("randnum", result.randnum)
        trans_list = block_dict.get("transactions", [])    
        if trans_list:
            result.set_head_transaction(Transaction.load_trans(trans_list[0]))
            for trans in trans_list[1:]:
                t = Transaction.load_trans(trans)
                result.add_transaction(t)
        return result

    def set_index(self, index: int) -> None:
        """设置索引"""
        self.index = index

    def get_index(self) -> int:
        """获取index"""
        return self.index

    def clear_transactions(self) -> None:
        """清空交易"""
        self.transactions = []

    def get_transactions(self) -> List[Transaction]:
        """获取全部交易（包括第一笔交易）"""
        return [self.head_trans] + self.transactions

    def get_user_transactions(self) -> List[Transaction]:
        """获取用户的全部交易（不包括第一笔交易）"""
        return self.transactions

    def get_transaction(self, trans: int) -> Transaction:
        """获取第trans个交易"""
        if trans == 1:
            return self.head_trans
        else:
            return self.transactions[trans - 2]

    def get_transactions_length(self) -> int:
        """获取交易数量"""
        return len(self.get_transactions())

    def get_input(self, trans: int, inp: int) -> TransInput:
        """获取第trans笔交易、inp个输入"""
        return self.get_transaction(trans).get_input(inp)
    
    def get_output(self, trans: int, outp: int) -> TransOutput:
        """获取第trans笔交易、outp个输出"""
        return self.get_transaction(trans).get_output(outp)

    def get_timestap(self) -> time.struct_time:
        """获取时间戳"""
        return time.localtime(self.timestap)

    def add_transaction(self, trans: Transaction) -> None:
        """添加交易"""
        self.transactions.append(trans)

    def set_head_transaction(self, trans: Transaction) -> None:
        """添加创块交易（包括交易费和矿工奖励）"""
        self.head_trans = trans

    def get_head_transaction(self) -> Transaction:
        """获取创块交易"""
        return self.head_trans

    def get_now_ming_btcs(self) -> Btc:
        """计算当前区块时的矿工奖励"""
        tap = 2**(self.get_index() // REDUCE_BTCS_HEIGHT)
        mini_btcs = Btc(MINING_BTCS) / Btc(str(tap))
        return mini_btcs

    def get_prehash(self) -> str:
        """获取pre_hash"""
        return self.pre_hash

    def set_prehash(self, pre_hash: str) -> None:
        """设置区块的pre_hash"""
        self.pre_hash = pre_hash

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
            self.timestap = time.time()

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
            value = [str(self.head_trans)] + [str(tap) for tap in value]
        return value

    def __str__(self) -> str:
        return json.dumps(dict(self)).replace(" ", "")

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __ne__(self, other) -> bool:
        return str(self) != str(other)


if __name__ == "__main__":
    from .trans_input import TransInput
    from .trans_output import TransOutput
    from .btc import Btc
    from key import UserKey
    trans = Transaction()
    trans.add_input(TransInput(3, 5, 7))
    trans.add_output(TransOutput(Btc("5.67"), "fsfwetewtette4654654"))
    key = UserKey()
    trans.sign_transaction(key)
    trans2 = Transaction.load_trans(str(trans))
    trans2.add_input(TransInput(5, 6, 2))
    block = Block()
    block.add_transaction(trans)
    block.add_transaction(trans2)
    tap = str(block)
    print(tap)
    block2 = Block.load_block(tap)
    print(str(block2))
    print(str(block2) == str(block))
    block.find_randnum()
    print(block.get_hash())
