"""区块链的数据结构"""
from hashlib import sha256
from typing import Tuple, List, Set

from .trans_output import TransOutput
from .trans_input import TransInput
from .transaction import Transaction
from .block import Block


class BlockChain:
    """管理区块链的数据结构"""
    _instance = None

    def __init__(self) -> None:
        self.blocks: List[Block] = []       # 所有区块
        self.utxos: Set[str] = set()        # 所有未消费输出 "0-2-6"第0个区块，第2笔交易的第6个输出
        self.height = 0                     # 区块链高度
        self.hash = ""                      # 账本的hash值

    @classmethod
    def get_instance(cls) -> "BlockChain":
        """单例模式设计"""
        if cls._instance is None:
            cls._instance = BlockChain()
        return cls._instance

    def get_height(self) -> int:
        """获取区块链的高度"""
        return self.height

    def get_hash(self) -> str:
        """获取区块链的hash值"""
        if not self.hash:
            self.compute_hash()
        return self.hash

    def compute_hash(self) -> None:
        """计算区块链的hash值"""
        tap = "".join([str(block) for block in self.get_blocks()])
        tap += str(sorted(self.utxos))
        tap += str(self.height)
        self.hash = sha256(tap.encode("utf-8")).hexdigest()

    def get_block(self, block: int) -> Block:
        """获取第block个区块"""
        return self.blocks[block - 1]

    def get_blocks(self) -> List[Block]:
        """获取所有区块"""
        return self.blocks

    def get_transaction(self, block: int, trans: int) -> Transaction:
        """获取第block个区块、第trans笔交易"""
        return self.get_block(block).get_transaction(trans)

    def get_output(self, block: int, trans: int, outp: int) -> TransOutput:
        """定位到第block个区块、trans笔交易、outp个输出"""
        return self.get_block(block).get_output(trans, outp)
    
    def input_to_output(self, inp: TransInput) -> TransOutput:
        """根据输入找到输出"""
        return self.get_output(inp.block, inp.trans, inp.output)

    def get_input(self, block: int, trans: int, inp: int) -> TransInput:
        """定位到第block个区块、trans笔交易、inp个输出"""
        return self.get_block(block).get_input(trans, inp)

    def add_block(self, block: Block) -> None:
        """添加区块，并把区块中交易信息同步到utxo集中"""
        self.blocks.append(block)
        self.height += 1
        for i, trans in enumerate(block.get_transactions()):
            for inp in trans.get_inputs():                  # 移除已使用utxo
                self.utxos.remove(str(inp))
            for j, oup in enumerate(trans.get_outputs()):   # 添加新产生的utxo
                tap = f"{self.get_height()}-{i + 1}-{j + 1}"
                self.utxos.add(tap)
        self.compute_hash()

    def get_top_block(self) -> Block:
        """获取顶部区块"""
        return self.blocks[-1]
    
    def verify_utxo(self, block: int, trans: int, output: int) -> bool:
        """验证某个输出是否已被消费"""
        tap = f"{block}-{trans}-{output}"
        return tap in self.utxos


if __name__ == "__main__":
    from key import UserKey
    bc = BlockChain()
    key1 = UserKey()
    key2 = UserKey()
    t1 = Transaction()
    t1.add_output(TransOutput(50, key1.get_address()))
    t1.add_output(TransOutput(50, key2.get_address()))
    b1 = Block()
    b1.add_transaction(t1)
    b1.find_randnum()
    bc.add_block(b1)
    # key1向key2转账
    t2 = Transaction()
    t2.add_input(TransInput(0, 0, 0))
    t2.add_output(TransOutput(23.567, key2.get_address()))
    t2.sign_transaction(key1)
    b2 = Block()
    b2.add_transaction(t2)
    b2.find_randnum()
    bc.add_block(b2)
