"""配置文件"""
from decimal import Decimal

FIREST_BLOCK_PREHASH = "0" * 64         # 第一个区块的pre_hash的值

MAX_USER_TRANSACTION_NUMBER = 10        # 一个区块的用户交易最大数量

MIN_USER_TRANSACTION_NUMBER = 1         # 一个区块的用户交易最小数量

MIN_PRECISION_BTC = 8                   # btc的最小精度（小数点后8位）

HEAD_HASH = "000"                       # 挖矿难度（64位以内的16进制串，字母小写）

MINING_ADD_NUM = 0.0001                 # 找矿时的递增值

MINING_BTCS = Decimal("50")             # 矿工的的奖励

REDUCE_BTCS_HEIGHT = 210000             # 每多少个区块，矿工奖励减半
