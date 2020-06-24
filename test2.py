from chain import Transaction, Block, TransInput, TransOutput
from key import UserKey

# if __name__ == "__main__":
#     trans = Transaction()
#     trans.add_input(TransInput(3, 5, 7))
#     trans.add_output(TransOutput(5.67, "fsfwetewtette4654654"))
#     key = UserKey()
#     trans.sign_transaction(key)
#     print(str(trans))
#     print(trans.to_string_without_sign())
#     trans2 = Transaction(trans=str(trans))
#     print(trans2 == trans)
#     print(trans2.verify_transaction(key))
#     print(str(trans2) == str(trans))

if __name__ == "__main__":
    trans = Transaction()
    trans.add_input(TransInput(3, 5, 7))
    trans.add_output(TransOutput(5.67, "fsfwetewtette4654654"))
    key = UserKey()
    trans.sign_transaction(key)
    trans2 = Transaction(str(trans))
    trans2.add_input(TransInput(5, 6, 2))
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
