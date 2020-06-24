import json
from typing import List


class TransOutput:
    """交易输出"""
    def __init__(self, btcs: float=0, address: str="", trans_output: str="") -> None:
        """初始化"""
        self.btcs = btcs
        self.address = address
        if trans_output:
            self.load_output(trans_output)
    
    def load_output(self, trans_output: str) -> None:
        output_dict = json.loads(trans_output)
        self.btcs = output_dict.get("btcs", self.btcs)
        self.address = output_dict.get("address", self.address)

    def keys(self) -> List[str]:
        return [
            "btcs",
            "address"
        ]
    
    def __getitem__(self, key: str) -> int:
        return getattr(self, key)
    
    def __str__(self) -> str:
        return json.dumps(dict(self)).replace(" ", "")
