"""完整的区块链数据库"""
from decimal import Decimal

from chain import BlockChain


__all__ = ["FullBlockChain", ]


class FullBlockChain:
    """完整的账本"""
    def __init__(self) -> None:
        self.blc = BlockChain.get_instance()
    
    def set_blockchain(self, blc: BlockChain) -> None:
        """设定区块链数据库"""
        self.blc = blc
    
    def lookup_balance(self, address: str) -> Decimal:
        """查找一个地址的余额"""
        return self.blc.get_balance(address)
    

