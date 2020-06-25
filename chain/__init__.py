"""区块链的整体数据结构"""
# 区块中的序列从1开始计算
from .trans_input import TransInput
from .trans_output import TransOutput
from .transaction import Transaction
from .block import Block
from .blockchain import BlockChain


__all__ = ["TransInput", "TransOutput", "Transaction", "Block", "BlockChain", ]
