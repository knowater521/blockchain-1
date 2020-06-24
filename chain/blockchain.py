"""区块链的数据结构"""
from typing import Tuple, List, Set

from .trans_output import TransOutput
from .trans_input import TransInput
from .transaction import Transaction
from .block import Block


class BlockChain:
    """管理区块链的数据结构"""
    def __init__(self) -> None:
        self.blocks: List[Block] = []            # 所有区块
        self.utxos: Set[str] = set()          # 所有未消费输出 "0-2-6"第0个区块，第2笔交易的第6个输出
    
    def get_block(self, block: int) -> Block:
        """获取第block个区块"""
        return self.blocks[block]

    def get_transaction(self, block: int, trans: int) -> Transaction:
        """获取第block个区块、第trans笔交易"""
        return self.get_block(block).get_transaction(trans)

    def get_output(self, block: int, trans: int, outp: int) -> TransOutput:
        """定位到第block个区块、trans笔交易、outp个输出"""
        return self.get_block(block).get_output(trans, outp)
    
    def get_input(self, block: int, trans: int, inp: int) -> TransInput:
        """定位到第block个区块、trans笔交易、inp个输出"""
        return self.get_block(block).get_input(trans, inp)

    def add_block(self, block: Block) -> None:
        """添加区块，并把区块中交易信息同步到utxo集中"""
        self.blocks.append(block)
        # TODO
        for trans in block.get_transactions():
            for inp in trans.get_inputs():
                pass
            for oup in trans.get_outputs():
                pass


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
    t1.add_output(50, key1.get_address())
    t1.add_output(50, key2.get_address())
    b1 = Block()
    b1.add_transaction(t1)
    b1.find_randnum()
    bc.add_block(b1)
    # key1向key2转账
    t2 = Transaction()
    t2.add_input(0, 0, 0)
    t2.add_output(23.567, key2.get_address())
    t2.sign_transaction(key1)
    b2 = Block()
    b2.add_transaction(t2)
    b2.find_randnum()
    bc.add_block(b2)
