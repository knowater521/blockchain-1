from key import UserKey
from chain import TransOutput, TransInput, Transaction, Block, BlockChain
from config import MINING_BTCS
from verify import Verify

if __name__ == "__main__":
    # 创建区块链
    bc = BlockChain.get_instance()
    print(bc.get_start_time())
    # 初始的两个用户
    key1 = UserKey()
    key2 = UserKey()
    # 初始区块的创币交易（只有输出，没有输入）
    t1 = Transaction()
    t1.add_output(TransOutput(5000, key1.get_address()))
    t1.add_output(TransOutput(5000, key2.get_address()))
    # 创世区块
    b1 = Block()
    b1.add_transaction(t1)
    # 添加矿工奖励交易
    mt1 = Transaction()
    mt1.add_output(TransOutput(MINING_BTCS, key1.get_address()))
    b1.set_head_transaction(mt1)
    b1.set_index(1)
    # 挖矿
    b1.find_randnum()
    # 添加区块
    bc.add_block(b1)
    # key1向key2转账
    t2 = Transaction()
    t2.add_input(TransInput(1, 1, 1))
    t2.add_output(TransOutput(23.567, key2.get_address()))
    t2.sign_transaction(key1)
    if not Verify.verify_transaction(t2):
        print("交易有问题")
    b2 = Block(pre_hash=b1.get_hash())
    b2.add_transaction(t2)
    mt2 = Transaction()
    mt2.add_output(TransOutput(MINING_BTCS, key2.get_address()))
    # 计算交易费
    fee = bc.compute_block_fee(b2)
    mt2.add_output(TransOutput(fee, key2.get_address()))

    b2.set_head_transaction(mt2)
    b2.set_index(2)
    b2.find_randnum()
    if not Verify.verify_block_depth(b2):
        print("区块有问题")
    bc.add_block(b2)
    if not Verify.verify_blockchain_depth(bc):
        print("区块链有问题")
