from config import NETWORK_ROUTING_PORT
from .network_routing import Message, Node


def broad_msg(msg: Message) -> None:
    """广播消息"""
    to_msg = Message(recieve="N", type_="PUT", data=str(msg))
    Node("localhost", NETWORK_ROUTING_PORT).send_msg(to_msg)  # 广播区块

