from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep


flag = True


def server2():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("0.0.0.0", 12000))
    server.listen(1)
    conn, addr = server.accept()
    while flag:
        data = ""
        while True:
            data += conn.recv(1024).decode("utf-8")
            if not data:
                break
        print(data)
    server.close()


def client():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(("127.0.0.1", 12000))
    while flag:
        client.send(b"abc")
        sleep(2)
    client.close()


if __name__ == "__main__":
    Thread(target=server2).start()
    Thread(target=client).start()
    sleep(8)
    flag = False
