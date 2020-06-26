"""矿工"""
from typing import Set

from chain import Block, Transaction


class Miner:
    def __init__(self) -> None:
        self.trans_cache: Set[str] = set()      # 交易池

    def mining(self, block: Block) -> Block:
        pass

    def add_trans(self, trans: Transaction) -> None:
        """往交易池中添加交易"""
        self.trans_cache.add(str(trans))
    
    

