# 配置文件

配置说明

```python
FIREST_BLOCK_PREHASH = "0" * 64         # 第一个区块的pre_hash的值，r"[0-9a-f]{64}"

MAX_USER_TRANSACTION_NUMBER = 10        # 一个区块的用户交易最大数量，不包括创币交易

MIN_USER_TRANSACTION_NUMBER = 1         # 一个区块的用户交易最小数量

MIN_PRECISION_BTC = 8                   # btc的最小精度（小数点后8位）

HEAD_HASH = "000"                       # 挖矿难度，r"[0-9a-f]{1,64}"，越长越难

MINING_ADD_NUM = 0.0001                 # 找矿时的递增值

MINING_BTCS = "50"                      # 矿工的的奖励，只要能转换成Decimal数字就行

REDUCE_BTCS_HEIGHT = 210000             # 每过多少个区块，矿工奖励减半，第210000个区块就会减半
```

