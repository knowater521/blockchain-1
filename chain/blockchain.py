"""区块链的数据结构"""
from typing import Tuple

from .transaction import Transaction
from .block import Block


class BlockChain:
    """管理区块链的数据结构"""
    def __init__(self) -> None:
        self.blocks = []            # 所有区块
        self.valid_trans = set()    # 所有未消费输出 "0-2-6"第0个区块，第2笔交易的第6个输出
    
    def get_output(self, block: int, trans: int, output: int) -> Tuple[float, str]:
        """定位到第block个区块、trans笔交易、output个输出，返回值和地址"""
        tap = self.blocks[block].get_transaction(trans).get_output(output)
        return tap.get("btcs"), tap.get("address")
    
    def add_block(self, block: Block) -> None:
        """添加区块"""
        self.blocks.append(block)

    def get_top_block(self) -> Block:
        """获取顶部区块"""
        return self.blocks[-1]
    
    def verify_utxo(self, block: int, trans: int, output: int) -> bool:
        """验证某个输出是否已被消费"""
        tap = f"{block}-{trans}-{output}"
        return tap in self.valid_trans
    

