"""完整的区块链数据库B，必须有N以支持此功能"""
from typing import Dict
from collections import defaultdict
from contextlib import contextmanager
from queue import Queue

from chain import Btc, TransOutput, Block, BlockChain
from verify import Verify
from .network_routing import NetworkRouting

__all__ = ["FullBlockChain", ]


class FullBlockChain:
    """完整的账本，类似代理，确保同步"""
    def __init__(self) -> None:
        self.msgs: Queue[str] = Queue()     # 消息队列
        self.server_flag = True

    @property
    def __blc(self) -> BlockChain:
        return BlockChain.get_instance()
    
    def set_blockchain(self, blc: BlockChain) -> None:
        """设定区块链数据库"""
        BlockChain.set_instance(blc)
    
    def lookup_utxo(self, *address: str) -> Dict[str, TransOutput]:
        """查找一个或多个地址的utxo"""
        return self.__blc.get_utxo(*address)
    
    def lookup_balance(self, *address: str) -> Dict[str, Btc]:
        """查找一个或多个地址的余额"""
        result = defaultdict(Btc)
        for outp in self.lookup_utxo(*address).values():
            result[outp.address] += outp.btcs
        return result

    def get_hash(self) -> str:
        """获取本账本的hash值"""
        return self.__blc.get_hash()

    def get_height(self) -> int:
        """获取本账本的高度"""
        return self.__blc.get_height()

    def get_top_hash(self) -> str:
        """获取顶部区块的hash"""
        return self.__blc.get_top_block().get_hash()

    def add_new_block(self, block: Block) -> bool:
        """添加新块（带验证），验证通过则广播"""
        if Verify.verify_new_block(block):
            self.__blc.add_block(block)
            NetworkRouting.get_instance().add_a_msg(block)  # 广播区块
            return True
        return False

