from queue import Queue


__all__ = ["MyQueue", ]


class MyQueue(Queue):
    """线程安全队列"""
    def __init__(self, maxsize=0) -> None:
        """设定队列最大item数量"""
        super().__init__(maxsize)
    
    def contain(self, item) -> bool:
        """检查item是否在queue中"""
        with self.mutex:
            return item in list(self.queue)

