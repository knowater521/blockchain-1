"""
对区块链的相关操作
ip格式为：0.0.0.0:5000
"""
import traceback
from internet import get_list_from_url
from block import veri_block_hash, com_block_hash
from transaction import verify_transaction, veri_reward_trans, un_standard_transaction

def veri_newblock_forchain(chain_list, block_dict):
    """验证新区块的有效性"""
    # 如果是创世区块
    if len(chain_list) == 0 and block_dict["index"] == 0:
        return True
    last_block = chain_list[-1]
    # 新区块的index值应符合规定
    if not block_dict["index"] == last_block["index"] + 1:
        return False
    # 新区块的hash应符合规定
    if not veri_block_hash(block_dict):
        return False
    # 新区块应指向last_block
    if not block_dict["pre_hash"] == com_block_hash(last_block):
        return False
    # copy一份
    trans_list = block_dict["transactions"][:]
    for i, trans_dict in enumerate(trans_list):
        trans_list[i] = trans_dict.copy()
    # 检查矿工奖励
    if not veri_reward_trans(trans_list[0]):
        return False
    # 检查剩下的交易
    trans_list = trans_list[1:]
    # 区块中的一般交易不能超过10笔
    if len(trans_list) > 10:
        return False
    # 还原区块中的交易为原始交易
    for i, trans_dict in enumerate(trans_list):
        trans_list[i] = un_standard_transaction(trans_dict)
    # 区块中的交易应有效
    if not verify_transaction(chain_list, *trans_list):
        return False
    return True

def update_blockchain(chain_list, block_dict):
    """用新区块更新区块链"""
    # 把新区块中的交易输入对应的utxo设为False
    for trans_dict in block_dict["transactions"]:
        in_utxos = trans_dict["inputs"]
        for inp in in_utxos:
            block_index, trans_index, export_index = inp["block"], inp["trans"], inp["export"]
            chain_list[block_index]["transactions"][trans_index]["outputs"][export_index]["valid"] = False
    # 加入新区块
    chain_list.append(block_dict)
    return chain_list

def get_blockchain_from_ip(ip):
    """从地址为ip的节点中获取blockchain"""
    url = "http://" + ip + "/blockchain"
    newchain =  get_list_from_url(url)
    return newchain

def veri_blockchain(chain):
    """验证区块链的有效性"""
    # 验证区块的hash值
    for ch in chain:
        if not veri_block_hash(ch):
            return False
    # 验证区块的连接性
    for i in range(1, len(chain)):
        block_hash1 = com_block_hash(chain[i-1])
        block_hash2 = chain[i]["pre_hash"]
        if block_hash1 != block_hash2:
            return False
    return True
