"""完整的区块链数据库"""
from typing import List

from chain import Btc, TransOutput, BlockChain


__all__ = ["FullBlockChain", ]


class FullBlockChain:
    """完整的账本"""
    def __init__(self) -> None:
        self.blc = BlockChain.get_instance()
    
    def set_blockchain(self, blc: BlockChain) -> None:
        """设定区块链数据库"""
        self.blc = blc
    
    def lookup_utxo(self, *address: str) -> List[TransOutput]:
        """查找一个或多个地址的utxo"""
        return self.blc.get_utxo(*address)
    
    def lookup_balance(self, *address: str) -> Btc:
        """查找一个或多个地址的余额"""
        result = Btc("0")
        for outp in self.lookup_utxo(*address):
            result += outp.btcs
        return result

