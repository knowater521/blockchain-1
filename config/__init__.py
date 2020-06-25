"""配置文件"""

# 第一个区块的pre_hash的值
FIREST_BLOCK_PREHASH = "0" * 64
# 一个区块的用户交易最大数量
MAX_USER_TRANSACTION_NUMBER = 10
# 一个区块的用户交易最小数量
MIN_USER_TRANSACTION_NUMBER = 1
# 挖矿难度（64位以内的16进制串，字母小写）
HEAD_HASH = "000"
# 找矿时的递增值
MINING_ADD_NUM = 0.0001
# 矿工的的奖励
MINING_BTCS = 50
# 每多少个区块，矿工奖励减半
REDUCE_BTCS_HEIGHT = 210000
