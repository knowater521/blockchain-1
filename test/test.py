# 发起交易的测试
from peer import Peer
from transaction import Transaction
from key import create_key, address_key

p = Peer()
p.add_friend("127.0.0.1:5000")
p.sync_blockchain()

pub_str, pri_str = create_key()

trans = Transaction()
trans.add_input(0, 0, 0)
trans.add_output(15.3545, address_key(pub_str))
trans.set_cost(0.003)
diff = trans.com_insum_outsum(p.get_blockchain())


file = open("pub.key", "r")
pub_key = file.read()
file.close()
file = open("pri.key", "r")
pri_key = file.read()
file.close()
trans.add_output(diff, address_key(pub_key))    # 余额
trans.sign_transaction(pub_key, pri_key)
trans_dict = trans.derive_transaction()
print(trans_dict["sign"])

if p.add_transaction(trans_dict):
    p.send_transaction(trans_dict)
