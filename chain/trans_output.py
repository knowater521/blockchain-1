"""交易输出的数据结构"""
from decimal import Decimal
from typing import List

from .btc import Btc


__all__ = ["TransOutput", ]


class TransOutput:
    """交易输出"""
    def __init__(self, btcs: Decimal=Btc("0"), address: str="", trans_output: str="") -> None:
        """初始化"""
        self.btcs = btcs
        self.address = address
        if trans_output:
            self.load_output(trans_output)
    
    def load_output(self, trans_output: str) -> None:
        tap = trans_output.split("-")
        self.btcs = Btc((tap[0]))
        self.address = tap[1]

    def keys(self) -> List[str]:
        return [
            "btcs",
            "address"
        ]
    
    def __getitem__(self, key: str) -> int:
        return getattr(self, key)
    
    def __str__(self) -> str:
        """btcs-address"""
        tap = str(self.btcs).strip("0")
        if tap:
            tap = "0"
        return f"{tap}-{self.address}"
    
    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __ne__(self, other) -> bool:
        return str(self) != str(other)
