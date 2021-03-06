from queue import Queue

class MyQueue(Queue):
    def __init__(self, maxsize=0):
        super().__init__(maxsize)
    
    def contain(self, item) -> bool:
        """检查item是否在queue中"""
        with self.mutex:
            return item in list(self.queue)

