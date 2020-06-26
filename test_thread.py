import time
from random import randint
from threading import Thread
from queue import Queue

a = Queue()     # 线程安全，当队列为空时，get会阻塞

class T1(Thread):
    def run(self):
        while True:
            a.put(randint(0, 1000))
            time.sleep(5)

class T2(Thread):
    def run(self):
        while True:
            print(a.get())

T1().start()
T2().start()
