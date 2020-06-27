"""验证用户交易合法性"""
import re

from chain import Btc, Transaction, BlockChain
from .base import BaseTransVerify


__all__ = ["TransVerify", ]


class InpOutpTrans(BaseTransVerify):
    """输入输出的验证"""
    def __init__(self, trans: Transaction) -> None:
        super().__init__(trans)
    
    def is_ok(self) -> bool:
        # 输入的值应合法
        inputs = self.trans.get_inputs()
        for inp in inputs:
            if inp.block <= 0 or inp.trans <= 0 or inp.output <= 0:
                return False
        # 输入的值不能有重复的
        if len(set(inputs)) != len(inputs):
            return False
        # 输出的值应合法
        for outp in self.trans.get_outputs():
            if outp.btcs <= Btc("0") or not re.match(r"[0-9a-f]{64}", outp.address):
                return False
        return True


class FormatTrans(BaseTransVerify):
    """交易格式的验证"""
    def __init__(self, trans: Transaction) -> None:
        super().__init__(trans)
    
    def is_ok(self) -> bool:
        # 输入不能为空
        if not self.trans.get_inputs():
            return False
        # 输出不能为空
        if not self.trans.get_outputs():
            return False
        # 必须签名
        if not self.trans.get_pub_keys() or not self.trans.get_signeds():
            return False
        return True


class SignedTrans(BaseTransVerify):
    """交易签名的验证"""
    def __init__(self, trans: Transaction) -> None:
        super().__init__(trans)
    
    def is_ok(self) -> bool:
        address_list = [key.get_address() for key in self.trans.get_pub_keys()]
        # 签名必须有效
        if not self.trans.verify_transaction():
            return False
        # 每一个输入都为本人的utxo
        for inp in self.trans.get_inputs():
            outp = BlockChain.get_instance().input_to_output(inp)
            if outp.address not in address_list:
                return False
        return True


class AmountTrans(BaseTransVerify):
    """交易金额的验证"""
    def __init__(self, trans: Transaction) -> None:
        super().__init__(trans)
    
    def is_ok(self) -> bool:
        # 交易费必须大于0
        blc = BlockChain.get_instance()
        return blc.compute_transaction_fee(self.trans) > Btc("0")


TransVerify = [InpOutpTrans, FormatTrans, SignedTrans, AmountTrans]
