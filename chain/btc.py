"""底层货币单位"""
from decimal import Decimal

from config import MIN_PRECISION_BTC


__all__ = ["Btc", ]


class Btc:
    def __init__(self, value: str="0") -> None:
        value = self.__format_value(value)
        self.value = round(Decimal(value), MIN_PRECISION_BTC)    # 四舍五入

    @staticmethod
    def __format_value(value: str) -> str:
        value = value.strip().lstrip("0")
        if "." in value:
            value = value.rstrip("0")
        if value == "" or value == ".":
            value = "0"
        return value

    def __float__(self) -> float:
        """值"""
        return float(self.value)

    def __int__(self) -> int:
        """整数"""
        return int(self.value)

    def __add__(self, other: "Btc") -> "Btc":
        """加法"""
        return Btc(str(self.value + other.value))

    def __sub__(self, other: "Btc") -> "Btc":
        """减法"""
        return Btc(str(self.value - other.value))
    
    def __mul__(self, other: "Btc") -> "Btc":
        """乘法"""
        return Btc(str(self.value * other.value))

    def __truediv__(self, other: "Btc") -> "Btc":
        """除法"""
        return Btc(str(self.value / other.value))

    def __floordiv__(self, other: "Btc") -> "Btc":
        """整除"""
        return Btc(str(self.value // other.value))

    def __mod__(self, other: "Btc") -> "Btc":
        """取模"""
        return Btc(str(self.value % other.value))

    def __pow__(self, other: "Btc") -> "Btc":
        """幂运算"""
        return Btc(str(self.value**other.value))

    def __eq__(self, other) -> bool:
        """=="""
        return str(self) == str(other)
    
    def __ne__(self, other) -> bool:
        """!="""
        return str(self) != str(other)

    def __lt__(self, other) -> bool:
        """<"""
        return self.value < other.value
    
    def __gt__(self, other) -> bool:
        """>"""
        return self.value > other.value
    
    def __le__(self, other) -> bool:
        """<="""
        return self.value <= other.value
    
    def __ge__(self, other) -> bool:
        """>="""
        return self.value >= other.value

    def __str__(self) -> str:
        return self.__format_value(str(self.value))
    
    def __repr__(self) -> str:
        return str(self)


if __name__ == "__main__":
    print(Btc("223.00000003") / Btc("0.1"), 223.00000003 / 0.1)
    print(Btc("0.0000004") + Btc("1.001"), 0.0000004 + 1.001)
    print(Btc("0.00003") - Btc("12.1111"), 0.00003 - 12.1111)
    print(Btc("2.33") * Btc("4.5551"), 2.33 * 4.5551)
    print(Btc("45.3") // Btc("9.0"), 45.3 // 9)

