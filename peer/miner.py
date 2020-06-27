"""矿工"""
from typing import Set, List
from threading import Thread

from config import MAX_USER_TRANSACTION_NUMBER
from chain import Btc, Block, Transaction, BlockChain, TransOutput
from verify import Verify
from .network_routing import NetworkRouting

__all__ = ["Miner", ]


class Miner:
    def __init__(self) -> None:
        self.trans_cache: Set[Transaction] = set()      # 交易池
        self.trans_num = MAX_USER_TRANSACTION_NUMBER    # 一个区块打包多少个交易
        self.address = ""           # 获取收益的地址
        self.server_flag = True

    def mining(self, block: Block) -> Block:
        """挖矿"""
        trans_list = self.__get_mining_trans()
        blc = BlockChain.get_instance()
        block = Block(blc.get_height() + 1, blc.get_top_block().get_hash())
        # 计算总交易费
        fee = Btc("0")
        for trans in trans_list:
            fee += blc.compute_transaction_fee(trans)
            block.add_transaction(trans)    # 添加交易到block中
        # 加上矿工奖励
        fee += block.get_now_ming_btcs()
        # 构造创块交易
        head_trans = Transaction()
        head_trans.add_output(TransOutput(address=self.address, btcs=fee))
        block.set_head_transaction(head_trans)
        # 正式开始挖矿
        block.find_randnum()
        return block

    def add_trans(self, trans: Transaction) -> bool:
        """往交易池中添加交易（先验证）""" 
        if trans not in self.trans_cache and Verify.verify_new_transaction(trans):
            self.trans_cache.add(trans)
            return True
        return False

    def __get_mining_trans(self) -> List[Transaction]:
        """获取用于打包区块的交易"""
        trans_list = []
        for i in range(self.trans_num):
            tap = self.trans_cache.pop()
            trans_list.append(tap)
        return trans_list

    def accept_block(self, block: Block) -> None:
        """胜利者已经产生（新块已加入区块链）"""
        # TODO 广播新块
        # TODO 停止挖矿

    def start_server(self) -> None:
        self.server_flag = True
        N = NetworkRouting.get_instance()
        def recv_broad_transaction():
            """接收交易、广播交易的进程"""
            trans_tap = N.get_a_msg(Transaction)
            trans = Transaction.load_trans(trans_tap)
            if self.add_trans(trans):
                N.add_a_msg(trans)
        def mining_broad_block():
            """挖矿、广播新块的进程"""
            # TODO
        recv_thread = Thread(target=recv_broad_transaction, name="Miner recv_broad_transaction Thread", daemon=True)
        recv_thread.start()
        mining_thread = Thread(target=mining_broad_block, name="Miner mining_broad_block Thread", daemon=True)
        mining_thread.start()

    def close_server(self) -> None:
        self.server_flag = False
        pass    # TODO
