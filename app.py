from time import sleep

from key import UserKey
from chain import BlockChain, Block, Transaction, TransOutput, Btc
from peer import NetworkRouting, FullBlockChain, Miner, Wallet
from config import NETWORK_ROUTING_PORT, MINING_BTCS


if __name__ == "__main__":
    NetworkRouting.get_instance().start_server()
    FullBlockChain.get_instance().start_server()
    Miner.get_instance().start_server()
    W = Wallet(Btc("2"))
    keys = [UserKey() for i in range(10)]
    for key in keys:
        W.add_key(key)
    Miner.get_instance().set_wallet_address(keys[0].get_address())
    sleep(2)

    t = Transaction()
    for key in keys:
        t.add_output(TransOutput(Btc("100"), key.get_address()))
    block = Block(1)
    block.add_transaction(t)
    head_trans = Transaction()
    head_trans.add_output(TransOutput(Btc(MINING_BTCS), keys[0].get_address()))
    block.set_head_transaction(head_trans)
    block.find_randnum()
    BlockChain.get_instance().add_block(block)
    W.sync_balance()
    trans = W.pay({keys[1].get_address(): Btc("30")})
    W.broad_a_trans(trans)
    
    sleep(8)
    print(BlockChain.get_instance().get_height())



