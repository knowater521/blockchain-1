"""网络路由N"""
from .node import Node
from .message import Message
from .server import N_server, M_mailbox, B_mailbox, W_mailbox, N_mailbox
from .network import NetworkRouting


__all__ = ["Node", "Message", "N_server", "NetworkRouting", "N_mailbox", "M_mailbox", "B_mailbox", "W_mailbox"]


def broad_msg(msg: Message) -> None:
    """广播消息"""
    to_msg = Message(recieve="N", type_="PUT", data=str(msg))
    N_mailbox.put(to_msg)  # 广播区块

