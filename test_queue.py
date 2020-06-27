from queue import Queue
from collections import defaultdict

if __name__ == "__main__":
    a = defaultdict(Queue)
    a["测试"].put("你好")
    print(a["测试"].get())


