"""网络中的消息"""
import json
from typing import Any, List


__all__ = ["Message", ]


RECIEVES = ["W", "N", "M", "B", "*"]
TYPE = ["GET", "PUT", "RESPONSE", "NONE"]
COMMAND = [""]
STATE = [200, 404]


class Message:
    def __init__(self, recieve=RECIEVES[-1], type_=TYPE[-1], command=COMMAND[-1], data="") -> None:
        self.recieve = recieve      # 接收者，消息会被上传到节点的哪一部分功能
        self.type = type_           # 类型
        self.command = command      # 消息的额外指令
        self.data = data            # 消息附带的数据
        self.state = 200            # 消息的状态
    
    @classmethod
    def load(cls, msg: str) -> "Message":
        msg_dict = json.loads(msg)
        result = cls()
        for k, v in msg_dict.items():
            setattr(result, k, v)
        return result

    def set_state(self, state: int) -> None:
        self.state = state

    def keys(self) -> List[str]:
        return [
            "recieve",
            "type",
            "command",
            "data",
            "state",
        ]

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
    
    def __str__(self) -> str:
        return json.dumps(dict(self)).replace(" ", "")

    def __hash__(self) -> int:
        return hash(str(self))
