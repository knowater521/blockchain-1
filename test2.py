from chain import *
from key import *


if __name__ == "__main__":
    trans = Transaction()
    trans.add_input(TransInput(3, 5, 7))
    trans.add_output(TransOutput(Btc("5.67"), "fsfwetewtette4654654"))
    key = UserKey()
    trans.sign_transaction(key)
    trans2 = Transaction.load_trans(str(trans))
    trans2.add_input(TransInput(5, 6, 2))
    block = Block()
    block.add_transaction(trans)
    block.add_transaction(trans2)
    tap = str(block)
    print(tap)
    block2 = Block.load_block(tap)
    print(str(block2))
    print(str(block2) == str(block))
    block.find_randnum()
    print(block.get_hash())
