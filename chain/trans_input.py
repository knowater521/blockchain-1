"""交易输入的数据结构"""
from typing import List


__all__ = ["TransInput", ]


class TransInput:
    """交易输入"""
    def __init__(self, block: int=0, trans: int=0, output: int=0, trans_input: str="") -> None:
        """初始化"""
        self.block = block
        self.trans = trans
        self.output = output
        if trans_input:
            self.load_input(trans_input)
    
    def load_input(self, trans_input: str) -> None:
        tap = trans_input.split("-")
        self.block = int(tap[0])
        self.trans = int(tap[1])
        self.output = int(tap[2])

    def keys(self) -> List[str]:
        return [
            "block",
            "trans",
            "output"
        ]
    
    def __getitem__(self, key: str) -> int:
        return getattr(self, key)
    
    def __str__(self) -> str:
        """block-trans-output"""
        return f"{self.block}-{self.trans}-{self.output}"
