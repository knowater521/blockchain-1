"""钱包"""
from typing import List

from key import UserKey

class Wallet:
    def __init__(self) -> None:
        self.user_keys: List[UserKey] = []  # 存储用户的密钥


    