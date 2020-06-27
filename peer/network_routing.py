"""网络路由"""
from typing import Set

class NetworkRouting:
    def __init__(self) -> None:
        self.nodes: Set[str] = set()        # 本机连接的节点
    
    def add_node(self, node: str) -> None:
        self.nodes.add(node)
    
    def remove_node(self, node: str) -> None:
        self.nodes.remove(node)
    
    

