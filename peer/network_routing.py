"""网络路由"""
from typing import Set, Tuple
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from config import NETWORK_ROUTING_PORT, NETWORK_ROUTING_ADDRESS, NETWORK_ROUTING_SERVER_NUM


class NetworkRouting:
    def __init__(self) -> None:
        self.nodes: Set[Node] = set()        # 本机连接的节点 {("127.0.0.1", 3347), }
        self.blacklist: Set[Node] = set()    # 黑名单（拒绝这些节点的连接）
        self.client = socket(AF_INET, SOCK_STREAM)      # client socket
        self.server = socket(AF_INET, SOCK_STREAM)      # server socket
        self.server.bind((NETWORK_ROUTING_ADDRESS, NETWORK_ROUTING_PORT))
        self.server.listen(NETWORK_ROUTING_SERVER_NUM)
    
    def add_node(self, node: str) -> None:
        """增加新节点"""
        self.nodes.add(Node.load_node(node))
    
    def remove_node(self, node: str) -> None:
        """移除节点"""
        self.nodes.remove(Node.load_node(node))
    
    def add_node_toblacklist(self, node: str) -> None:
        """增加黑名单"""
        self.blacklist.add(Node.load_node(node))

    def broadcast_info(self, info: str) -> None:
        """广播信息"""
        for node in self.nodes:
            if not node.send_info(self.client, info):
                print("Errror on connect to host:", str(node))

    def start_server(self) -> None:
        """打开服务"""
        flag = True
        def run():
            while flag:
                conn, addr = self.server.accept()
                data_list = []
                while True:
                    data = conn.recv(1024).decode("utf-8")
                    if not data:
                        break
                    data_list.append(data)
                data = "".join(data_list)
                # TODO 处理请求
        t = Thread(target=run)
        t.setDaemon(True)
        t.start()


class Node:
    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port
    
    @classmethod
    def load_node(cls, node: str) -> "Node":
        name, port = node.split(":")
        return cls(name, int(port))

    def send_info(self, socket: socket, info: str) -> bool:
        """发送信息给node"""
        try:
            socket.connect((self.name, self.port))
            socket.sendall(info.encode("utf-8"))
            socket.close()
            return True
        except Exception as e:
            return False

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return f"{self.name}:{self.port}"
