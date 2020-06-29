from threading import Thread, Condition
from itertools import chain
import abc
import sys

STOP = False    # 停止标志

class BuffBlock:
    """缓冲区的类"""
    def __init__(self, num: int) -> None:
        self.number = num       # 缓冲区块号，从1开始
        self.next = None        # 下一个缓冲区
        self.content = ''       # 保存内容的部分


class BlockQueue:
    """缓冲队列，每个列元素都是缓冲区"""
    def __init__(self) -> None:
        self.RS = 0         # 资源信号量
        self.RS_cond = Condition()  # 因等待RS信号量而阻塞的线程队列
        self.MS = 1         # 互斥信号量
        self.MS_cond = Condition()  # 因等待MS信号量而阻塞的线程队列
        h = BuffBlock(0)    # 代表空值
        self.head = h       # 队首指针
        self.tail = h       # 队尾指针

    def put(self, block: BuffBlock) -> None:
        # 队列元素增加，队尾指针后移
        self.tail.next = block
        self.tail = block
    
    def get(self) -> BuffBlock:
        if self.head.next is not None:
            # 取出队列首部元素，队首指针后移
            t = self.head.next
            self.head.next = None
            self.head = t
            return t
        else:
            # 在信号量的机制下可以确保不触发此异常
            raise RuntimeError('队列已空')


class BuffPool:
    """缓冲池，有固定数量的缓冲区"""
    def __init__(self, num: int) -> None:
        # 建立固定数量的缓冲区
        self.blocks = []
        for i in range(num):
            self.blocks.append(BuffBlock(i+1))
        # 把缓冲区全部挂在emq队列上
        self.emq = BlockQueue()
        for block in self.blocks:
            self.emq.put(block)
            self.emq.RS += 1
        # inq和outq初始均为空
        self.inq = BlockQueue()
        self.outq = BlockQueue()



class MyThread(Thread, metaclass=abc.ABCMeta):
    """添加了对缓冲区操作的线程"""
    def __init__(self, pool: BuffPool) -> None:
        super().__init__()
        self.pool = pool    # 缓冲池

    def getbuf(self, queue: BlockQueue) -> BuffBlock:
        queue.RS_cond.acquire()
        # Wait队列的RS信号量
        queue.RS -= 1
        if queue.RS < 0:
            queue.RS_cond.wait()
        # Wait队列的MS信号量
        if queue.MS == 0:
            queue.RS_cond.wait()
        queue.MS = 0
        # 获取buf
        tap = queue.get()      # 工作缓冲区
        # 释放MS信号量
        queue.MS = 1
        queue.RS_cond.release()
        return tap

    def putbuf(self, queue: BlockQueue, tap: BuffBlock) -> None:
        queue.RS_cond.acquire()
        # Wait队列的MS信号量
        if queue.MS == 0:
            queue.RS_cond.wait()
        queue.MS = 0
        # 添加buf
        queue.put(tap)
        # 释放MS信号量
        queue.MS = 1
        # 释放RS信号量
        queue.RS += 1
        if queue.RS < 1:
            queue.RS_cond.notify(1)
        queue.RS_cond.release()



class InputThread(MyThread):
    """输入进程"""
    def __init__(self, pool: BuffPool) -> None:
        super().__init__(pool)

    def run(self):
        while not STOP:
            # 收容输入
            hin = self.getbuf(self.pool.emq)    # 收容输入工作缓冲区
            hin.content = input()
            self.putbuf(self.pool.inq, hin)
        print('****输入进程结束****')



class ComputeThread(MyThread):
    """计算进程"""
    def __init__(self, pool: BuffPool) -> None:
        super().__init__(pool)

    def run(self):
        global STOP
        while not STOP:
            # 提取输入
            sin = self.getbuf(self.pool.inq)    # 提取输入工作缓冲区
            content = sin.content
            sin.content = ''
            self.putbuf(self.pool.emq, sin)
            # 判断程序是否结束
            if content == 'exit':
                STOP = True
            # 收容输出
            hout = self.getbuf(self.pool.emq)   # 收容输出工作缓冲区
            hout.content = content.upper()
            self.putbuf(self.pool.outq, hout)
        print('****计算进程结束****')



class OutputThread(MyThread):
    """输出进程"""
    def __init__(self, pool: BuffPool) -> None:
        super().__init__(pool)

    def run(self):
        while not STOP:
            # 提取输出
            sout = self.getbuf(self.pool.outq)  # 提取输出工作缓冲区
            content = sout.content
            sout.content = ''
            print(content)
            self.putbuf(self.pool.emq, sout)
        print('****输出进程结束****')



if __name__ == "__main__":
    pool = BuffPool(50)     # 建立有50个缓冲区的缓冲池
    # 建立输入、计算、输出进程
    t_input = [InputThread(pool)]
    t_compute = [ComputeThread(pool) for i in range(2)]
    t_output = [OutputThread(pool) for i in range(2)]
    # 启动进程
    for i in chain(t_input, t_compute, t_output):
        i.start()

