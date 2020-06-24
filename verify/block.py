"""验证区块的合法性"""
from chain import Block
from config import MAX_TRANSACTION_NUMBER
from .base import BaseBlockVerify


__all__ = ["BlockVerify", ]


class FormatBlock(BaseBlockVerify):
    """区块格式的验证"""
    def __init__(self, block: Block) -> None:
        super().__init__(block)
    
    def is_ok(self) -> bool:
        # 单个区块的交易数量不能超过上限，也不能为空
        tr_len = len(self.block.get_transactions())
        if tr_len > MAX_TRANSACTION_NUMBER or tr_len == 0:
            return False
        return True


class HashBlock(BaseBlockVerify):
    """区块hash值的验证"""
    def __init__(self, block: Block) -> None:
        super().__init__(block)
    
    def is_ok(self) -> bool:
        return self.block.veri_hash()


BlockVerify = [FormatBlock, HashBlock]