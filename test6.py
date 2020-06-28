from peer import NetworkRouting


if __name__ == "__main__":
    with NetworkRouting.safe_use_networkrouting() as N:
        N.start_server()
        N.add_node("127.0.0.1:2020")
        N.broadcast_info("你好")
        N.broadcast_info("不好")
        N.broadcast_info("还好")
        print(N.get_a_msg())
        N.close_server()
        N.broadcast_info("发不出去")
        N.broadcast_info("发不出去")
        N.broadcast_info("发不出去")
