import os

from config import STORE_DIR, MINING_BTCS
from key import UserKey
from chain import Btc, Transaction, TransOutput, Block
from peer import NetworkRouting, FullBlockChain, Wallet, Miner


def init():
    # 检查文件夹
    if not os.path.isdir(STORE_DIR):
        os.mkdir(STORE_DIR)
    # 打开N服务和B服务
    NetworkRouting.get_instance().start_server()
    FullBlockChain.get_instance().start_server()
    # 添加创世区块
    keys = [UserKey() for i in range(10)]
    for key in keys:
        Wallet.get_instance().add_key(key)
    Miner.get_instance().set_wallet_address(keys[0].get_address())
    t = Transaction()
    for key in keys:
        t.add_output(TransOutput(Btc("1000"), key.get_address()))
    block = Block(1)
    block.add_transaction(t)
    head_trans = Transaction()
    head_trans.add_output(TransOutput(Btc(MINING_BTCS), keys[0].get_address()))
    block.set_head_transaction(head_trans)
    block.find_randnum()
    FullBlockChain.get_instance().add_first_block(block)

if __name__ == "__main__":
    init()
