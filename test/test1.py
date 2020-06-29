from chain import *
from key import *


if __name__ == "__main__":
    trans = Transaction()
    trans.add_input(TransInput(3, 5, 7))
    trans.add_output(TransOutput(Btc("5.67"), "fsfwetewtette4654654"))
    key = UserKey()
    key2 = UserKey()
    key3 = UserKey()
    trans.sign_transaction(key)
    trans.sign_transaction(key2)
    trans.sign_transaction(key3)
    print(str(trans))
    print(trans.to_string_without_sign())
    trans2 = Transaction.load_trans(str(trans))
    print(trans2 == trans)
    print(trans2.verify_transaction())
    print(str(trans2) == str(trans))
