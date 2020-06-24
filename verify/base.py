"""verify的基类"""
import abc

from chain import Transaction


class BaseTransVerify(metaclass=abc.ABCMeta):
    def __init__(self, trans: Transaction) -> None:
        self.trans = trans
    
    @abc.abstractmethod
    def is_ok(self) -> bool:
        pass
