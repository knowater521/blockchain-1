"""完整的区块链数据库"""
from typing import Dict
from collections import defaultdict

from chain import Btc, TransOutput, Block, BlockChain
from verify import Verify


__all__ = ["FullBlockChain", ]


class FullBlockChain:
    """完整的账本"""
    def __init__(self) -> None:
        pass

    @property
    def blc(self) -> BlockChain:
        return BlockChain.get_instance()
    
    def set_blockchain(self, blc: BlockChain) -> None:
        """设定区块链数据库"""
        BlockChain.set_instance(blc)
    
    def lookup_utxo(self, *address: str) -> Dict[str, TransOutput]:
        """查找一个或多个地址的utxo"""
        return self.blc.get_utxo(*address)
    
    def lookup_balance(self, *address: str) -> Dict[str, Btc]:
        """查找一个或多个地址的余额"""
        result = defaultdict(Btc)
        for outp in self.lookup_utxo(*address).values():
            result[outp.address] += outp.btcs
        return result

    def get_hash(self) -> str:
        """获取本账本的hash值"""
        return self.blc.get_hash()

    def get_height(self) -> int:
        """获取本账本的高度"""
        return self.blc.get_height()

    def add_new_block(self, block: Block) -> bool:
        """添加新块（带验证）"""
        if Verify.verify_new_block(block):
            self.blc.add_block(block)
            return True
        return False

    # TODO 同步主链
    # TODO 查询服务
