"""N服务"""
from typing import Tuple
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from config import NETWORK_ROUTING_ADDRESS, NETWORK_ROUTING_PORT, NETWORK_ROUTING_SERVER_NUM
from .node import Node
from .message import Message


__all__ = ["N_server", "N_mailbox", "W_mailbox", "B_mailbox", "M_mailbox", ]


N_mailbox = Queue()        # N的信箱
W_mailbox = Queue()        # W的信箱
B_mailbox = Queue()        # B的信箱
M_mailbox = Queue()        # N的信箱

POST_OPTION = {
    "N": N_mailbox,
    "W": W_mailbox,
    "B": B_mailbox,
    "M": M_mailbox
}


class N_server:
    __recv_server_flag = True
    __send_server_flag = True
    __postman_server_flag = True
    __recv_msg_queue = Queue() # 接收消息队列，源node，msg
    __send_msg_queue = Queue() # 发送消息队列，目标node，msg

    @classmethod
    def start_recv_msg_server(cls) -> None:
        cls.__recv_server_flag = True
        def run():
            """接收消息线程"""
            server = socket(AF_INET, SOCK_STREAM)
            server.bind((NETWORK_ROUTING_ADDRESS, NETWORK_ROUTING_PORT))
            server.listen(NETWORK_ROUTING_SERVER_NUM)
            while cls.__recv_server_flag:
                conn, addr = server.accept()
                data_list = []
                while True:
                    data = conn.recv(1024).decode("utf-8")
                    if not data:
                        break
                    data_list.append(data)
                data = "".join(data_list)
                msg = Message.load(data)
                cls.__recv_msg_queue.put((Node(addr[0], addr[1]), msg))
        thread = Thread(target=run, daemon=True, name="-N recv server thread-")
        thread.start()

    @classmethod
    def start_send_msg_server(cls) -> None:
        cls.__send_server_flag = True
        def run():
            """发送消息线程"""
            while cls.__send_msg_queue:
                node, msg = cls.__send_msg_queue.get()
                node.send_msg(msg)
        thread = Thread(target=run, daemon=True, name="-N send server thread-")
        thread.start()

    @classmethod
    def start_postman_server(cls) -> None:
        cls.__postman_server_flag = True
        def run():
            while cls.__postman_server_flag:
                node, msg = cls.__recv_msg_queue.get()
                if msg.recieve in POST_OPTION.keys():
                    POST_OPTION[msg.recieve].put((node, msg))
        thread = Thread(target=run, daemon=True, name="-N postman server thread-")
        thread.start()

    @classmethod
    def start_server(cls) -> None:
        cls.start_send_msg_server()
        cls.start_recv_msg_server()
        cls.start_postman_server()
    
    @classmethod
    def stop_recv_msg_server(cls) -> None:
        cls.__recv_server_flag = False
        Node("localhost", NETWORK_ROUTING_PORT).send_msg(Message())
    
    @classmethod
    def stop_send_msg_server(cls) -> None:
        cls.__send_server_flag = False
        cls.__send_msg_queue.put((Node("localhost", NETWORK_ROUTING_PORT), Message()))

    @classmethod
    def stop_postman_server(cls):
        cls.__postman_server_flag = False
        cls.__recv_msg_queue.put((Node("localhost", NETWORK_ROUTING_PORT), Message()))

    @classmethod
    def stop_server(cls) -> None:
        cls.stop_send_msg_server()
        cls.stop_recv_msg_server()
        cls.stop_postman_server()

    @classmethod
    def send_a_msg(cls, node: Node, msg: Message) -> None:
        cls.__send_msg_queue.put((node, msg))

