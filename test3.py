from key import UserKey
from chain import TransOutput, TransInput, Transaction, Block, BlockChain

if __name__ == "__main__":
    bc = BlockChain()
    key1 = UserKey()
    key2 = UserKey()
    t1 = Transaction()
    t1.add_output(TransOutput(50, key1.get_address()))
    t1.add_output(TransOutput(50, key2.get_address()))
    b1 = Block()
    b1.add_transaction(t1)
    b1.find_randnum()
    bc.add_block(b1)
    # key1向key2转账
    t2 = Transaction()
    t2.add_input(TransInput(1, 1, 1))
    t2.add_output(TransOutput(23.567, key2.get_address()))
    t2.sign_transaction(key1)
    b2 = Block(pre_hash=b1.get_hash())
    b2.add_transaction(t2)
    b2.find_randnum()
    bc.add_block(b2)
