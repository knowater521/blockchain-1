"""矿工M，必须有B和N以支持此功能"""
import time
from typing import Set, List, Optional
from threading import Thread, Condition, Lock
from contextlib import contextmanager

from config import MAX_USER_TRANSACTION_NUMBER, MINING_ADD_NUM
from chain import Btc, Block, Transaction, TransOutput
from verify import Verify
from .network_routing import NetworkRouting
from .fullblockchain import FullBlockChain


__all__ = ["Miner", ]


class Miner:
    def __init__(self) -> None:
        self.trans_cache: Set[Transaction] = set()      # 交易池
        self.trans_num = MAX_USER_TRANSACTION_NUMBER    # 一个区块打包多少个交易
        self.address = ""                               # 获取收益的地址
        self.server_flag = True
        self.mine_flag = True
        self.use_cond = Condition()     # 占用等待队列
        self.use_num = 1                # 占用信号量
        self.consum_cond = Condition()  # 消费等待队列
        self.consum_num = 0             # 消费需求的信号量
        self.lock = Lock()

    @contextmanager
    def __safe_occupy(self):
        """安全使用（独占）"""
        self.condition.acquire()
        with self.lock:
            self.trans_cond -= 1
        if self.trans_cond < 0:
            self.condition.wait()
        yield
        with self.lock:
            self.trans_cond += 1
        if self.trans_cond < 1:
            self.condition.notify(1)
        self.condition.release()

    @contextmanager
    def __safe_consum(self):
        """安全使用（取出）"""
        self.consum_cond.acquire()
        with self.lock:
            self.consum_num -= 1
        if self.consum_num < 0:
            self.consum_cond.wait()
        yield
        self.consum_cond.release()

    def add_trans(self, *transes: Transaction) -> bool:
        """往交易池中添加交易（先验证）""" 
        with self.__safe_occupy():
            result = False
            for trans in transes:
                if trans not in self.trans_cache and Verify.verify_new_transaction(trans):
                    self.trans_cache.add(trans)
                    with self.lock:
                        self.consum_num += 1
                    if self.consum_num < 1:     # 如果有因get而阻塞的线程，则唤醒
                        self.consum_cond.notify(1)
                    result = True
        return result

    def get_trans(self) -> Transaction:
        """从交易池中取一个交易（阻塞）"""
        with self.__safe_consum():
            with self.__safe_occupy():
                tap = self.trans_cache.pop()
        return tap

    def remove_trans(self, *transes: Transaction) -> None:
        """从交易池中移除交易"""
        with self.__safe_occupy():
            for trans in transes:
                if trans in self.trans_cache:
                    self.trans_cache.remove(trans)
                    self.consum_num -= 1

    def __get_mining_trans(self) -> List[Transaction]:
        """获取用于打包区块的交易"""
        trans_list = []
        for i in range(self.trans_num):
            tap = self.get_trans()
            trans_list.append(tap)
        return trans_list

    def __mining(self) -> Optional[Block]:
        """挖矿"""
        trans_list = self.__get_mining_trans()
        with FullBlockChain.safe_use_blockchain() as blc:
            block = Block(blc.get_height() + 1, blc.get_top_hash())
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
        while not block.veri_hash():
            if self.mine_flag:
                block.randnum += MINING_ADD_NUM
                block.timestap = time.time()
            else:       # 中止挖矿（失败了）
                self.add_trans(*trans_list)     # 把交易放回交易池
                return None
        return block

    def accept_block(self, block: Block) -> None:
        """胜利者已经产生（新块已加入区块链）"""
        self.suspend_mining()
        self.remove_trans(*block.get_user_transactions())

    def start_server(self) -> None:
        """打开服务"""
        self.server_flag = True
        N = NetworkRouting.get_instance()
        def recv_broad_transaction():
            """接收交易、广播交易的进程"""
            while self.server_flag:     # 阻塞在取trans的地方
                trans_tap = N.get_a_msg(Transaction)
                trans = Transaction.load_trans(trans_tap)
                if self.add_trans(trans):
                    N.add_a_msg(trans)
        def mining_broad_block():
            """挖矿、广播新块的进程"""
            self.mine_flag = True
            while self.server_flag and self.mine_flag:
                block = self.__mining()
                if block is not None:
                    with FullBlockChain.safe_use_blockchain() as blc:
                        blc.add_new_block(block)
        recv_thread = Thread(target=recv_broad_transaction, name="Miner recv_broad_transaction Thread", daemon=True)
        recv_thread.start()
        mining_thread = Thread(target=mining_broad_block, name="Miner mining_broad_block Thread", daemon=True)
        mining_thread.start()

    def suspend_mining(self) -> None:
        """中止挖矿"""
        self.mine_flag = False
        self.add_trans(Transaction())

    def close_server(self) -> None:
        """关闭服务"""
        self.server_flag = False
        NetworkRouting.get_instance().add_a_msg(Transaction())
        self.suspend_mining()
