from chain.transaction import Transaction
from key import UserKey

if __name__ == "__main__":
    trans = Transaction()
    trans.add_input(3, 5, 7)
    trans.add_output(5.67, "fsfwetewtette4654654")
    key = UserKey()
    trans.sign_transaction(key)
    print(trans.to_string())
    print(trans.to_string_without_sign())
    trans2 = Transaction(trans.to_string())
    print(trans2 == trans)
    print(trans2.verify_transaction(key))
    print(trans2.to_string() == trans.to_string())
