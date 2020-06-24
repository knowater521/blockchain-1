import json
from typing import List


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
        input_dict = json.loads(trans_input)
        self.block = input_dict.get("block", self.block)
        self.trans = input_dict.get("trans", self.trans)
        self.output = input_dict.get("output", self.output)

    def keys(self) -> List[str]:
        return [
            "block",
            "trans",
            "output"
        ]
    
    def __getitem__(self, key: str) -> int:
        return getattr(self, key)
    
    def __str__(self) -> str:
        return json.dumps(dict(self)).replace(" ", "")
