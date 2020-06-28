from time import sleep

from peer.network_routing import NetworkRouting, Message, Node
from peer.fullblockchain import FullBlockChain
from peer.miner import Miner
from config import NETWORK_ROUTING_PORT


if __name__ == "__main__":
    NetworkRouting.get_instance().start_server()
    FullBlockChain.get_instance().start_server()
    M = Miner()
    M.start_server()
    sleep(2)

    msg = Message(recieve="B", type_="PUT", data="测试")
    msg_2 = Message(recieve="N", type_="PUT", data=str(msg))
    Node("localhost", NETWORK_ROUTING_PORT).send_msg(msg_2)

    sleep(4)



