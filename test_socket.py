from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep


flag = True
num = 0


def server2():
    global num
    server = socket(AF_INET, SOCK_STREAM)
    server.settimeout(2)
    server.bind(("0.0.0.0", 12000))
    server.listen(1)
    while flag:
        conn, addr = server.accept()
        data_list = []
        while True:
            data = conn.recv(1024).decode("utf-8")
            num += 1
            if not data:
                break
            data_list.append(data)
        data = "".join(data_list)
        if data:
            print(data)
    server.close()


def client2():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(("127.0.0.1", 12000))
    for i in range(10):
        client.send(b"abc")
    client.close()


if __name__ == "__main__":
    t1 = Thread(target=server2)
    t2 = Thread(target=client2)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    sleep(3)
    t2.start()
    sleep(8)
    flag = False
    print(num)
    # client = socket(AF_INET, SOCK_STREAM)
    # client.connect(("www.baidu.com", 80))
    # client.connect(("www.oct-month.top", 80))
    # client.close()
