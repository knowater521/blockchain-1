"""验证区块的合法性"""
from typing import List

from chain import Block
from config import MAX_USER_TRANSACTION_NUMBER, MIN_USER_TRANSACTION_NUMBER
from .base import BaseBlockVerify


__all__ = ["BlockVerify", ]


class HashBlock(BaseBlockVerify):
    """区块hash值的验证"""
    def __init__(self, block: Block) -> None:
        super().__init__(block)
    
    def is_ok(self) -> bool:
        return self.block.veri_hash()


class FormatBlock(BaseBlockVerify):
    """区块格式的验证"""
    def __init__(self, block: Block) -> None:
        super().__init__(block)
    
    def is_ok(self) -> bool:
        # 单个区块的用户交易数量不能超过上限，也不能小于下限
        tr_len = len(self.block.get_user_transactions())
        if tr_len > MAX_USER_TRANSACTION_NUMBER or tr_len < MIN_USER_TRANSACTION_NUMBER:
            return False
        return True


BlockVerify: List[type] = [HashBlock, FormatBlock]
