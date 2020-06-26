from chain import *
from key import *


if __name__ == "__main__":
    trans = Transaction()
    trans.add_input(TransInput(3, 5, 7))
    trans.add_output(TransOutput(Btc("5.67"), "fsfwetewtette4654654"))
    key = UserKey()
    trans.sign_transaction(key)
    print(str(trans))
    print(trans.to_string_without_sign())
    trans2 = Transaction.load_trans(str(trans))
    print(trans2 == trans)
    print(trans2.verify_transaction(key))
    print(str(trans2) == str(trans))
