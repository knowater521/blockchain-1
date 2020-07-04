from PyQt5.Qt import QObject


__all__ = ["TimingEvent", ]


class TimingEvent(QObject):
    """定时事件"""
    def __init__(self, caller) -> None:
        super().__init__()
        self.caller = caller

    def set_caller(self, caller) -> None:
        self.caller = caller

    def timerEvent(self, _) -> None:
        self.caller()
