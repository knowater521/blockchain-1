"""verify的基类"""
import abc

from chain import Transaction, Block


class BaseVerify(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_ok(self) -> bool:
        pass


class BaseTransVerify(BaseVerify):
    def __init__(self, trans: Transaction) -> None:
        self.trans = trans


class BaseBlockVerify(BaseVerify):
    def __init__(self, block: Block) -> None:
        self.block = block

