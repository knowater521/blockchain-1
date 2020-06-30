"""完整的区块链数据库B，必须有N以支持此功能"""
from typing import Dict
from collections import defaultdict
from contextlib import contextmanager
from queue import Queue
from threading import Thread

from config import NETWORK_ROUTING_PORT
from chain import Btc, TransOutput, Block, BlockChain, Transaction
from verify import Verify
from .network_routing import Node, Message, B_mailbox, NetworkRouting


__all__ = ["FullBlockChain", ]


class FullBlockChain:
    __instance = None

    """完整的账本，类似代理，确保同步"""
    def __init__(self) -> None:
        self.server_flag = True

    @classmethod
    def get_instance(cls) -> "FullBlockChain":
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

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
        result: Dict[str, Btc] = defaultdict(Btc)
        for outp in self.lookup_utxo(*address).values():
            result[outp.address] += outp.btcs
        return result

    def compute_transaction_fee(self, trans: Transaction) -> Btc:
        """计算一笔交易的交易费"""
        return self.__blc.compute_transaction_fee(trans)

    def get_utxo(self, *address) -> Dict[str, TransOutput]:
        """查找一个或多个地址的utxo"""
        return self.__blc.get_utxo(*address)

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
            msg = Message(recieve="B", type_="PUT", data=str(block))
            to_msg = Message(recieve="N", type_="PUT", data=str(msg))
            Node("localhost", NETWORK_ROUTING_PORT).send_msg(to_msg)  # 广播区块
            return True
        return False

    def start_server(self) -> None:
        """启动B服务"""
        self.server_flag = True
        def run():
            """接收区块，广播区块线程"""
            node, msg = B_mailbox.get()
            if msg.type == "PUT":   
                if msg.command == "BLOCK":      # 添加新块，广播新块
                    block = Block.load(msg.data)
                    if self.add_new_block(block):
                        NetworkRouting.get_instance().broad_a_msg(msg)
            elif msg.type == "GET":
                pass    # TODO
        thread = Thread(target=run, daemon=True, name="-B server thread-")
        thread.start()


