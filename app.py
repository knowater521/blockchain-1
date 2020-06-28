from time import sleep

from key import UserKey
from chain import BlockChain, Block, Transaction, TransOutput, Btc
from peer.network_routing import NetworkRouting
from peer.fullblockchain import FullBlockChain
from peer.miner import Miner
from peer.wallet import Wallet
from config import NETWORK_ROUTING_PORT, MINING_BTCS


if __name__ == "__main__":
    NetworkRouting.get_instance().start_server()
    FullBlockChain.get_instance().start_server()
    M = Miner()
    M.start_server()
    W = Wallet()
    keys = [UserKey() for i in range(10)]
    for key in keys:
        W.add_key(key)
    M.set_wallet_address(keys[0].get_address())
    sleep(2)

    t = Transaction()
    for key in keys:
        t.add_output(TransOutput(Btc("100"), key.get_address()))
    block = Block(1)
    block.add_transaction(t)
    head_trans = Transaction()
    head_trans.add_output(TransOutput(Btc(MINING_BTCS), keys[0].get_address()))
    block.set_head_transaction(head_trans)
    block.find_num()
    BlockChain.get_instance().add_block(block)
    W.sync_balance()
    trans = W.pay({keys[1].get_address(): Btc("30")})
    M.add_trans(trans)

    sleep(4)



