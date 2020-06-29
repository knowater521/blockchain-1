"""交易输入的数据结构"""
from typing import List


__all__ = ["TransInput", ]


class TransInput:
    """交易输入"""
    def __init__(self, block: int=0, trans: int=0, output: int=0) -> None:
        """初始化"""
        self.block = block
        self.trans = trans
        self.output = output
    
    @classmethod
    def load_input(cls, trans_input: str) -> "TransInput":
        tap = trans_input.split(":")
        return cls(int(tap[0]), int(tap[1]), int(tap[2]))

    def keys(self) -> List[str]:
        return [
            "block",
            "trans",
            "output"
        ]
    
    def __getitem__(self, key: str) -> int:
        return getattr(self, key)
    
    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        """block-trans-output"""
        return f"{self.block}:{self.trans}:{self.output}"

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __ne__(self, other) -> bool:
        return str(self) != str(other)
