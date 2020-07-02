"""网络路由N"""
import json
from typing import Set, Dict, Tuple, Any, List
from threading import Thread

from config import NETWORK_ROUTING_PORT
from .node import Node
from .message import Message
from .server import N_server, N_mailbox


__all__ = ["NetworkRouting", ]


class NetworkRouting:
    __instance = None

    def __init__(self) -> None:
        self.nodes: Set[Node] = set()        # 本机连接的节点 {("127.0.0.1", 3347), }
        self.nodes.add(Node("localhost", NETWORK_ROUTING_PORT)) # 必然包括本机
        self.blacklist: Set[Node] = set()    # 黑名单（拒绝这些节点的连接）
        self.server_flag = True

    @classmethod
    def get_instance(cls) -> "NetworkRouting":
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def broad_a_msg(self, msg: Message) -> None:
        """广播一个消息"""
        for node in self.nodes:
            N_server.send_a_msg(node, msg)

    def get_nodes(self) -> List[str]:
        """拿到所有节点"""
        return [str(node) for node in self.nodes]

    def set_nodes(self, node_list: List[str]) -> None:
        """设定nodes"""
        self.clear_nodes()
        self.add_node(*node_list)

    def clear_nodes(self) -> None:
        """清空nodes"""
        self.nodes.clear()

    def add_node(self, *nodes: str) -> None:
        """增加新节点"""
        for node in nodes:
            try:
                self.nodes.add(Node.load(node))
            except Exception as e:
                print(e)
    
    def remove_node(self, node: str) -> None:
        """移除节点"""
        self.nodes.remove(Node.load(node))
    
    def add_node_toblacklist(self, node: str) -> None:
        """增加黑名单"""
        self.blacklist.add(Node.load(node))

    def start_server(self) -> None:
        """启动N服务"""
        N_server.start_server()
        def run():
            while self.server_flag:
                node, msg = N_mailbox.get()
                if msg.type == "GET":
                    data = json.dumps(self.get_nodes())
                    msg = Message(recieve="N", type_="RESPONSE", data=data)
                    node.send_msg(msg)
                elif msg.type == "PUT":
                    msg = Message.load(msg.data)
                    self.broad_a_msg(msg)
                elif msg.type == "RESPONSE":
                    pass    # TODO
            N_server.stop_server()
        thread = Thread(target=run, daemon=True, name="-N server thread-")
        thread.start()

    def stop_server(self) -> None:
        """停止服务"""
        self.server_flag = False
