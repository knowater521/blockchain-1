from chain import Btc, Transaction, Block, BlockChain
from config import MINING_BTCS, REDUCE_BTCS_HEIGHT
from .transaction import TransVerify
from .block import BlockVerify
from .blockchain import BlockChainVerify


__all__ = ["Verify", ]


class Verify:
    @staticmethod
    def verify_transaction(trans: Transaction) -> bool:
        """简单验证交易"""
        for verify in TransVerify:
            if not verify(trans).is_ok():
                return False
        return True

    @classmethod
    def verify_new_transaction(cls, trans: Transaction) -> bool:
        """验证一笔新交易"""
        if not cls.verify_transaction(trans):
            return False
        # 验证输入的有效性
        for inp in trans.get_inputs():
            if not BlockChain.get_instance().verify_utxo(inp.block, inp.trans, inp.output):
                return False
        return True

    @staticmethod
    def verify_block(block: Block) -> bool:
        """简单验证区块"""
        for verify in BlockVerify:
            if not verify(block).is_ok():
                return False
        return True
    
    @classmethod
    def verify_new_block(cls, block: Block) -> bool:
        """验证一个新块"""
        if not cls.verify_block_depth(block):
            return False
        # pre_hash的值要正确
        if block.get_prehash() != BlockChain.get_instance().get_top_block().get_hash():
            return False
        # 验证每笔交易的有效性
        inputs = []
        for trans in block.get_user_transactions():
            if not cls.verify_new_transaction(trans):
                return False
            inputs.extend(trans.get_inputs())
        # 不同的交易不能有相同的输入
        tap = [str(inp) for inp in inputs]
        if len(set(tap)) != len(tap):
            return False
        return True

    @staticmethod
    def verify_blockchain() -> bool:
        """简单验证区块链"""
        for verify in BlockChainVerify:
            if not verify().is_ok():
                return False
        return True

    @classmethod
    def verify_block_depth(cls, block: Block) -> bool:
        """深入验证区块（包括区块中的交易）"""
        if not cls.verify_block(block):
            return False
        # 验证用户的交易
        for trans in block.get_user_transactions():
            if not cls.verify_transaction(trans):
                return False
        # 验证第一笔交易
        trans = block.get_head_transaction()
        # 计算交易费
        fee = BlockChain.get_instance().compute_block_fee(block)
        # 计算矿工奖励
        mini_fee = trans.compute_outputs_btcs() - fee
        # 计算这个区块时的矿工奖励
        mini_btcs = block.get_now_ming_btcs()
        # 验证矿工奖励合法性
        if mini_fee != mini_btcs:
            return False
        return True
    
    @classmethod
    def verify_blockchain_depth(cls) -> bool:
        """深入验证区块链（区块、交易）"""
        if not cls.verify_blockchain():
            return False
        for block in BlockChain.get_instance().get_blocks()[1:]:      # 第一个区块不作检查
            if not cls.verify_block_depth(block):
                return False
        return True


