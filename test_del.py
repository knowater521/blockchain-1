class A:
    def __init__(self) -> None:
        print("create")
    
    def __del__(self) -> None:
        print("destroy")

A()
