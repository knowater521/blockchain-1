"""
对网络中节点的描述
"""
from blockchain import get_blockchain_from_ip, veri_blockchain, veri_newblock_forchain, update_blockchain
from transaction import verify_transaction, standard_transaction, create_reward_trans
from internet import send_dict_to_url, get_list_from_url
from block import Block, com_block_hash, create_new_block, find_answer_for_block

class Peer():
    """网络中的节点"""
    def __init__(self):
        self.blockchain = []        # 账本
        self.friends = set()        # 连接的节点
        self.trans_cache = []       # 交易池（set中不能存放dict数据）
    
    def add_friend(self, *friends):
        """添加节点"""
        for friend in friends:
            self.friends.add(friend)

    def sync_blockchain(self):
        """同步账本"""
        for peer in self.friends:
            newchain = get_blockchain_from_ip(peer)
            # 如果新链比自己的长并且有效
            if len(newchain) > len(self.blockchain) and veri_blockchain(newchain):
                self.blockchain = newchain
    
    def get_blockchain(self):
        """返回区块链"""
        return self.blockchain
    
    def get_trans_cache(self):
        """返回交易池"""
        return self.trans_cache
    
    def get_friend_peer(self):
        """返回节点连接的ip"""
        return list(self.friends)

    def get_trans_cache_height(self):
        """返回交易池中的交易数"""
        return len(self.trans_cache)
    
    def get_blockchain_height(self):
        """返回区块链的高度"""
        return len(self.blockchain)

    def gain_new_friend(self):
        """从已连接的节点中添加其它的节点"""
        for ip in self.friends:
            url = "http//" + ip + "/friends"
            ip_list = get_list_from_url(url)
            self.friends.update(ip_list)
    
    def add_transaction(self, trans_dict):
        """（先验证交易）添加交易到交易池中"""
        # 检查交易池中是否已存在此交易
        if trans_dict in self.trans_cache:
            return False
        # 检查交易的有效性
        cache = self.trans_cache[:]
        cache.append(trans_dict)
        if verify_transaction(self.blockchain, *cache):  # 待优化
            self.trans_cache.append(trans_dict)
            return True
        else:
            return False

    def send_transaction(self, trans_dict):
        """把交易分发给其它的节点"""
        for ip in self.friends:
            url = "http://" + ip + "/transactions"
            send_dict_to_url(url, trans_dict)

    def add_block(self, block_dict):
        """（先验证区块）向区块链中加入新的区块"""
        if veri_newblock_forchain(self.blockchain, block_dict):
            self.blockchain = update_blockchain(self.blockchain, block_dict)
            return True
        else:
            return False

    def package_send_block(self, pub_str):
        """打包新区块，然后挖矿、广播"""
        trans_list = self.trans_cache[:10]
        # 删除交易池中已取出的交易
        self.trans_cache = self.trans_cache[10:]
        block_dict = create_new_block(self.blockchain, pub_str, trans_list)
        # 添加区块并广播
        self.add_block(block_dict)
        self.send_block(block_dict)

    def send_block(self, block_dict):
        """把区块分发给其它的节点"""
        for ip in self.friends:
            url = "http://" + ip + "/blocks"
            send_dict_to_url(url, block_dict)

    # def broadcast_trans(self, trans_dict):
    #     """广播交易/发起交易"""
    #     self.add_transaction(trans_dict)
    #     self.send_transaction(trans_dict)