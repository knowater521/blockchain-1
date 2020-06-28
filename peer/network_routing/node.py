"""网络中的节点"""
from socket import socket, AF_INET, SOCK_STREAM

from config import NETWORK_TIMEOUT_SECS
from .message import Message


__all__ = ["Node", ]


class Node:
    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port
    
    @classmethod
    def load(cls, node: str) -> "Node":
        name, port = node.split(":")
        return cls(name, int(port))

    def send_msg(self, msg: Message) -> bool:
        """发送信息给node（可能失败）"""
        try:
            client = socket(AF_INET, SOCK_STREAM)      # client socket
            client.settimeout(NETWORK_TIMEOUT_SECS)
            client.connect((self.name, self.port))
            client.sendall(str(msg).encode("utf-8"))
            client.close()
            return True
        except Exception as e:
            return False

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return f"{self.name}:{self.port}"
