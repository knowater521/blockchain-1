"""钱包，必须有N以支持此功能"""
from typing import Set, Optional, List, Dict
from collections import defaultdict

from key import UserKey
from chain import Btc, TransInput, TransOutput, Transaction
from .fullblockchain import FullBlockChain


__all__ = ["Wallet", ]


class Wallet:
    """管理钱包"""
    def __init__(self) -> None:
        self.user_keys: Set[str] = set()                    # 存储用户的密钥
        self.trans_fee = Btc("0")                           # 预设的交易费
        self.balance: Dict[str, Btc] = defaultdict(Btc)     # 已知的地址对应的余额（缓存）
        self.utxos: Dict[str, TransOutput] = {}             # 可使用的utxo集

    def add_key(self, key: UserKey) -> None:
        """添加密钥"""
        self.user_keys.add(str(key))
    
    def set_trans_fee(self, fee: Btc) -> None:
        """设定交易费"""
        self.trans_fee = fee

    def get_key(self, address: str) -> Optional[UserKey]:
        """根据地址取出密钥"""
        for key in self.user_keys:
            user_key = UserKey.load_userkey(key)
            if address == user_key.get_address():
                return user_key
        return None

    def get_keys(self) -> List[UserKey]:
        """取出所有密钥"""
        return [UserKey.load_userkey(key) for key in self.user_keys]

    def remove_key(self, address: str) -> None:
        """根据地址移除密钥"""
        key = self.get_key(address)
        if key is not None:
            self.user_keys.remove(str(key))

    def sync_balance(self) -> None:
        """用blc更新钱包余额""" # TODO
        blc = FullBlockChain.get_instance()
        self.utxos = blc.get_utxo(*[user_key.get_address() for user_key in self.get_keys()])
        for outp in self.utxos.values():
            self.balance[outp.address] += outp.btcs

    def lookup_balance(self) -> Btc:
        """查看钱包余额"""
        result = Btc("0")
        for btc in self.balance.values():
            result += btc
        return result

    def pay(self, pay_to: Dict[str, Btc]) -> Transaction:
        """向一个或多个地址付钱（生成一笔交易）"""
        pay_sum = Btc("0")
        for value in pay_to.values():                          # 计算总的要付的钱
            pay_sum += value
        if self.lookup_balance() < pay_sum + self.trans_fee:    # 如果钱不够
            raise RuntimeError("number of btc is not enough!")
        # self.__sort_balance()
        address_set = set()
        pay_actually = Btc("0")
        t = Transaction()
        for address, btcs in pay_to.items():                    # 添加交易输出
            t.add_output(TransOutput(address=address, btcs=btcs))
        for inp, outp in self.utxos.items():                    # 添加交易输入
            address_set.add(outp.address)
            pay_actually += outp.btcs
            t.add_input(TransInput.load_input(inp))
            if pay_actually >= pay_sum + self.trans_fee:
                break
        pay_change = pay_actually - (pay_sum + self.trans_fee)  # 添加找零
        if pay_change != Btc("0"):
            user_key = UserKey()
            t.add_output(TransOutput(address=user_key.get_address(), btcs=pay_change))
            self.add_key(user_key)
        for address in address_set:                             # 签名
            tap_key = self.get_key(address)
            if tap_key is None:
                raise RuntimeError("wallet balance info is out-of-date!")
            t.sign_transaction(tap_key)
        return t
    
    def collect(self) -> str:
        """收钱（返回一个地址）"""
        user_key = UserKey()
        self.add_key(user_key)
        return user_key.get_address()
