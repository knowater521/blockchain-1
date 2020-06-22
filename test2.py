from chain import Transaction, Block
from key import UserKey


if __name__ == "__main__":
    trans = Transaction()
    trans.add_input(3, 5, 7)
    trans.add_output(5.67, "fsfwetewtette4654654")
    key = UserKey()
    trans.sign_transaction(key)
    trans2 = Transaction(str(trans))
    trans2.add_input(5, 6, 2)
    block = Block()
    block.add_transaction(trans)
    block.add_transaction(trans2)
    tap = str(block)
    print(tap)
    block2 = Block(block=tap)
    print(str(block2))
    print(str(block2) == str(block))
    block.find_randnum()
    print(block.get_hash())
