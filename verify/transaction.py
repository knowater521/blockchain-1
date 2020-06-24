"""验证交易合法性"""
from chain import Transaction, BlockChain
from .base import BaseTransVerify


__all__ = ["TransVerify", ]


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
        if not self.trans.get_pub_key() or not self.trans.get_signed():
            return False
        return True


class SignedTrans(BaseTransVerify):
    """交易签名的验证"""
    def __init__(self, trans: Transaction) -> None:
        super().__init__(trans)
    
    def is_ok(self) -> bool:
        address = self.trans.get_pub_key().get_address()
        # 签名必须有效
        if not self.trans.verify_transaction():
            return False
        # 每一个输入都为本人的utxo
        for inp in self.trans.get_inputs():
            blc = BlockChain.get_instance()
            outp = blc.input_to_output(inp)
            if not address == outp.address:
                return False
        return True


class AmountTrans(BaseTransVerify):
    """交易金额的验证"""
    def __init__(self, trans: Transaction) -> None:
        super().__init__(trans)
    
    def is_ok(self) -> bool:
        # 输入btcs必须大于输出btcs
        inp_btcs = 0.0
        for inp in self.trans.get_inputs():
            blc = BlockChain.get_instance()
            outp = blc.input_to_output(inp)
            inp_btcs += outp.btcs
        outp_btcs = 0.0
        for outp in self.trans.get_outputs():
            outp_btcs += outp.btcs
        return inp_btcs > outp_btcs


TransVerify = [FormatTrans, SignedTrans, AmountTrans]
