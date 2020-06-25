"""pass"""
from decimal import Decimal

from config import MIN_PRECISION_BTC


__all__ = ["Btc", ]


def Btc(value: str) -> Decimal:
    value = value.strip("0")
    return round(Decimal(value), MIN_PRECISION_BTC)


if __name__ == "__main__":
    print(Btc("223.00000003") / Btc("0.1"), 223.00000003 / 0.1)
    print(Btc("0.0000004") + Btc("1.001"), 0.0000004 + 1.001)
    print(Btc("0.00003") - Btc("12.1111"), 0.00003 - 12.1111)
    print(Btc("2.33") * Btc("4.5551"), 2.33 * 4.5551)
    print(Btc("45.3") // Btc("9.0"), 45.3 // 9)


# class Btc(value: str):
#     def __init__(self, value: str) -> None:
#         tap_value = round(Decimal(value), MIN_PRECISION_BTC)    # 四舍五入
#         self.sub_multiple = 10**MIN_PRECISION_BTC
#         self.virtual_value = int(tap_value * self.sub_multiple)
#         tap = 0
#         for i in reversed(str(self.virtual_value)):
#             if i == "0":
#                 tap += 0
#         tap = 10**tap
#         self.virtual_value //= tap
#         self.sub_multiple //= tap

#     def __float__(self) -> float:
#         """值"""
#         return self.virtual_value / self.sub_multiple

#     def __int__(self) -> int:
#         """整数"""
#         return self.virtual_value // self.sub_multiple

#     def __add__(self, other: "Btc") -> "Btc":
#         """加法"""
#         if self.sub_multiple > other.sub_multiple:
#             sub_m = self.sub_multiple // other.sub_multiple
#             result = (self.virtual_value + other.virtual_value * sub_m) / self.sub_multiple
#         else:
#             sub_m = other.sub_multiple // self.sub_multiple
#             result = (self.virtual_value * sub_m + other.virtual_value) / other.sub_multiple
#         return Btc(result)

#     def __sub__(self, other: "Btc") -> "Btc":
#         """减法"""
#         return self.__add__(Btc(-float(other)))
    
#     def __mul__(self, other: "Btc") -> "Btc":
#         """乘法"""
#         vir_value = self.virtual_value * other.virtual_value
#         sub_multi = self.sub_multiple * other.sub_multiple
#         return Btc(vir_value / sub_multi)

#     def __truediv__(self, other: "Btc") -> "Btc":
#         """除法"""
#         vir_value = self.virtual_value * other.sub_multiple
#         sub_multi = self.sub_multiple * other.virtual_value
#         return Btc(vir_value / sub_multi)

#     def __floordiv__(self, other: "Btc") -> "Btc":
#         """整除"""
#         vir_value = self.virtual_value * other.sub_multiple
#         sub_multi = self.sub_multiple * other.virtual_value
#         return Btc(vir_value // sub_multi)
    
#     def __mod__(self, other: "Btc") -> "Btc":
#         """取模"""
#         if self.sub_multiple > other.sub_multiple:
#             sub_m = self.sub_multiple // other.sub_multiple
#             result = (self.virtual_value % other.virtual_value * sub_m) / self.sub_multiple
#         else:
#             sub_m = other.sub_multiple // self.sub_multiple
#             result = (self.virtual_value * sub_m % other.virtual_value) / other.sub_multiple
#         return Btc(result)

#     def __pow__(self, other: "Btc") -> "Btc":
#         """幂运算"""
#         return Btc(float(self)**float(other))

#     def __str__(self) -> str:
#         return str(float(self))
    
#     def __repr__(self) -> str:
#         return str(self)
