"""钱包"""
from typing import Set, Optional, List, Dict

from key import UserKey
from chain import Btc, BlockChain, Transaction


__all__ = ["Wallet", ]


class Wallet:
    """管理钱包"""
    def __init__(self) -> None:
        self.user_keys: Set[str] = set()    # 存储用户的密钥

    def add_key(self, key: UserKey) -> None:
        """添加密钥"""
        self.user_keys.add(str(key))
    
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

    def lookup_balance(self, blc: BlockChain) -> Btc:
        """查看钱包余额"""
        result = Btc("0")
        utxos = blc.get_utxo(*[user_key.get_address() for user_key in self.get_keys()])
        for utxo in utxos:
            result += utxo.btcs
        return result

    def pay(self, pay_to: Dict[str, Btc]) -> List[Transaction]:
        """向一个或多个地址付钱"""
        # TODO


if __name__ == "__main__":
    wallet = Wallet()
    wallet.add_key(UserKey())
