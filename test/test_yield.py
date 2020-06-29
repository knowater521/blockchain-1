from contextlib import contextmanager

@contextmanager
def test():
    print("你好")
    yield 8
    print("再见")


if __name__ == "__main__":
    with test() as f:
        print(f)

