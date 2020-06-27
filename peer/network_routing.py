"""网络路由"""
from typing import Set, Tuple, List, Dict, Any
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue
from collections import defaultdict

from config import NETWORK_ROUTING_PORT, NETWORK_ROUTING_ADDRESS, NETWORK_ROUTING_SERVER_NUM, NETWORK_TIMEOUT_SECS


__all__ = ["NetworkRouting", ]


class NetworkRouting:
    __instance = None

    def __init__(self) -> None:
        self.nodes: Set[Node] = set()        # 本机连接的节点 {("127.0.0.1", 3347), }
        self.blacklist: Set[Node] = set()    # 黑名单（拒绝这些节点的连接）
        self.server_flag = True
        self.recv_msgs: Dict[str, Queue] = defaultdict(Queue)  # 接收消息队列，不同的消息对应不同的队列
        self.send_msgs: Queue[str] = Queue()    # 发送消息队列
    
    @classmethod
    def get_instance(cls) -> "NetworkRouting":
        """单例模式设计，全局唯一"""
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_a_msg(self, msg_type: type) -> str:
        """从消息队列中取一个消息（阻塞）"""
        return self.recv_msgs[msg_type.__name__].get()

    def add_a_msg(self, msg: Any) -> None:
        """发送一个消息给"""
        msg_head = type(msg).__name__       # 使用类名作为消息头
        self.send_msgs.put(msg_head + "-" + str(msg))

    def get_nodes(self) -> List[str]:
        """拿到所有节点"""
        return [str(node) for node in self.nodes]

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
            if not node.send_info(info):
                print("Errror on connect to host:", str(node))

    def start_server(self) -> None:
        """打开服务（守护线程）"""
        self.server_flag = True
        def recv_msg():
            """接收消息线程"""
            server = socket(AF_INET, SOCK_STREAM)      # server socket
            server.bind((NETWORK_ROUTING_ADDRESS, NETWORK_ROUTING_PORT))
            server.listen(NETWORK_ROUTING_SERVER_NUM)
            while self.server_flag:
                conn, addr = server.accept()
                if Node(*addr) in self.blacklist:   # 黑名单中的节点不提供服务
                    continue
                data_list = []
                while True:
                    data = conn.recv(1024).decode("utf-8")
                    if not data:
                        break
                    data_list.append(data)
                data = "".join(data_list)
                # 把收到的请求按请求头放到不同的消息队列里
                data_list = data.split("-")
                if len(data_list) >= 2:
                    msg_head = data_list[0]
                    msg_body = "".join(data_list[1:])
                    self.recv_msgs[msg_head].put(msg_body)
            server.close()
        def send_msg():
            """发送消息线程"""
            while self.server_flag:
                info = self.send_msgs.get() # 取出一条要发的消息
                for node in self.nodes:
                    if not node.send_info(info):
                        print("Errror on connect to host:", str(node))
        recv_thread = Thread(target=recv_msg, name="NetworkRouting recv_msg Thread", daemon=True)
        recv_thread.start()
        send_thread = Thread(target=send_msg, name="NetworkRouting send_msg Thread", daemon=True)
        send_thread.start()
    
    def close_server(self) -> None:
        """关闭服务"""
        self.server_flag = False
        Node("localhost", NETWORK_ROUTING_PORT).send_info("")


class Node:
    def __init__(self, name: str, port: int) -> None:
        self.name = name
        self.port = port
    
    @classmethod
    def load_node(cls, node: str) -> "Node":
        name, port = node.split(":")
        return cls(name, int(port))

    def send_info(self, info: str) -> bool:
        """发送信息给node"""
        try:
            client = socket(AF_INET, SOCK_STREAM)      # client socket
            client.settimeout(NETWORK_TIMEOUT_SECS)
            client.connect((self.name, self.port))
            client.sendall(info.encode("utf-8"))
            client.close()
            return True
        except Exception as e:
            return False

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return f"{self.name}:{self.port}"
