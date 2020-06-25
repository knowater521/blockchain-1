"""交易输出的数据结构"""
from typing import List


__all__ = ["TransOutput", ]


class TransOutput:
    """交易输出"""
    def __init__(self, btcs: float=0, address: str="", trans_output: str="") -> None:
        """初始化"""
        self.btcs = btcs
        self.address = address
        if trans_output:
            self.load_output(trans_output)
    
    def load_output(self, trans_output: str) -> None:
        tap = trans_output.split("-")
        self.btcs = float(tap[0])
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
        return f"{self.btcs}-{self.address}"
