"""矿工"""
from typing import Set, List
from queue import Queue

from config import MAX_USER_TRANSACTION_NUMBER
from chain import Block, Transaction


class Miner:
    def __init__(self) -> None:
        self.trans_cache = Queue()  # 交易池
        self.trans_num = MAX_USER_TRANSACTION_NUMBER    # 一个区块打包多少个交易

    def mining(self, block: Block) -> Block:
        """挖矿"""
        trans_list = self.get_mining_trans()
        pass

    def add_trans(self, trans: Transaction) -> None:
        """往交易池中添加交易"""
        # TODO
        self.trans_cache.put(trans)
    
    def get_mining_trans(self) -> List[Transaction]:
        """获取用于打包区块的交易（阻塞）"""
        trans_list = []
        for i in range(self.trans_num):
            tap = self.trans_cache.get()
            trans_list.append(tap)
        return trans_list

