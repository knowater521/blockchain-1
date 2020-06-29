"""
区块的数据结构
区块的相关操作
"""
"""
dict类型：
{
    "index": 0,                         # 索引
    "pre_hash": "j35jktj3i4tnf34itj3",  # 前一个区块的hash
    "timestap": 36454545.35435,         # 时间戳
    "answer": 34.35435,                 # 使区块满足某种条件的特殊float
    "transactions": [                   # 最多10条交易
        ...
    ]
}

"""
from time import time
import math
import hashlib
import re
from transaction import Transaction, verify_transaction, standard_transaction, create_reward_trans
from swap import dict_to_json
from key import address_key

class Block():
    """产生区块数据结构的模板"""
    def __init__(self, index, pre_hash):
        """产生一个区块模板"""
        self.index = index
        self.pre_hash = pre_hash
        self.timestap = time()
        self.answer = 0
        self.transactions = []
    
    def add_transactions(self, *trans_dicts):
        """添加交易"""
        for trans_dict in trans_dicts:
            if isinstance(trans_dict, dict):
                self.transactions.append(trans_dict)

    def export_dict(self):
        """导出区块字典"""
        block_dict = {
            "index": self.index,
            "pre_hash": self.pre_hash,
            "timestap": self.timestap,
            "answer": self.answer,
            "transactions": self.transactions
        }
        return block_dict


# 挖矿相关
def com_block_hash(block_dict):
    """计算区块的hash值"""
    block_str = dict_to_json(block_dict)
    block_bytes = block_str.encode("utf-8")
    block_hash = hashlib.sha256(block_bytes).hexdigest()
    return block_hash

def veri_block_hash(block_dict):
    """验证区块的hash值（设定挖矿难度）"""
    block_hash = com_block_hash(block_dict)
    if re.search("^0{4}", block_hash):
        return True
    else:
        return False

def find_answer_for_block(block_dict):
    """hash碰撞（挖矿）"""
    while not veri_block_hash(block_dict):
        block_dict["timestap"] = time()
        block_dict["answer"] += math.pi
    return block_dict

# 产生区块
def create_new_block(chain_list, pub_str, trans_list):
    """根据已有的链和传入的交易生成一个新的区块（挖矿）"""
    # 一个区块的交易不能超过10条
    if len(trans_list) > 10 or len(trans_list) < 1:
        return {}
    # 规范化所有的交易
    for i, trans in enumerate(trans_list):
        trans_list[i] = standard_transaction(trans, pub_str)
    # 添加矿工奖励
    reward = create_reward_trans(pub_str)
    trans_list.insert(0, reward)
    # 产生新区块
    new_block = Block(len(chain_list), com_block_hash(chain_list[-1]))
    new_block.add_transactions(*trans_list)
    block_dict = new_block.export_dict()
    # 挖矿
    block_dict = find_answer_for_block(block_dict)
    return block_dict

def create_first_block(*pub_pri_keys):
    """产生一个创世区块"""
    # pre_hash设定为全0，索引为0
    first_hash = "0"
    while len(first_hash) < 64:
        first_hash += "0"
    block = Block(0, first_hash)
    # 添加矿工奖励
    reward = create_reward_trans(pub_pri_keys[0][0])
    block.add_transactions(reward)
    # 初始的utxo
    for pub_str, pri_str in pub_pri_keys:
        trans = Transaction()
        trans.add_output(5000, address_key(pub_str))
        trans.sign_transaction(pub_str, pri_str)
        trans_dict = trans.derive_transaction()
        block.add_transactions(trans_dict)
    block_dict = block.export_dict()
    block_dict = find_answer_for_block(block_dict)
    return block_dict
