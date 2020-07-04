"""配置文件"""
import json
with open("./files/config/config.json", "r", encoding="utf-8") as f:
    try:
        config = json.loads(f.read())
    except Exception:
        config = {}

# 非程序文件的存放位置
STORE_DIR = config.get("STORE_DIR", "./files/")

# 程序GUI设定
WINDOW_TITLE = "BT币"
WINDOW_ICON = STORE_DIR + "img/main.ico"

# 秘钥的配置文件
STORE_KEYS_FILE_PATH = STORE_DIR + "user.keys"   # 持久化存储秘钥文件位置

# 底层区块链结构的配置
FIREST_BLOCK_PREHASH = "0" * 64         # 第一个区块的pre_hash的值，r"^[0-9a-f]{64}$"
MAX_USER_TRANSACTION_NUMBER = 1         # 一个区块的用户交易最大数量，不包括创币交易
MIN_USER_TRANSACTION_NUMBER = 1         # 一个区块的用户交易最小数量
MIN_PRECISION_BTC = 6                   # btc的最小精度（小数点后6位）
STORE_BLC_FILE_PATH = STORE_DIR + "blockchain.db"   # 持久化存储文件位置
DEFAULT_TRANS_FEE = config.get("DEFAULT_TRANS_FEE", "2")                 # 默认交易费

# 挖矿规则的配置
HEAD_HASH = "0000"                     # 挖矿难度，r"[0-9a-f]{1,64}"，越长越难
MINING_ADD_NUM = 0.0001                 # 找矿时的递增值
MINING_BTCS = "50"                      # 矿工的的奖励，只要能转换成Decimal数字就行
REDUCE_BTCS_HEIGHT = 210000             # 每多少个区块，矿工奖励减半，第210000个区块就会减半

# 路由服务的配置
NETWORK_ROUTING_ADDRESS = config.get("NETWORK_ROUTING_ADDRESS", "0.0.0.0")  # 路由服务监听地址
NETWORK_ROUTING_PORT = config.get("NETWORK_ROUTING_PORT", 2020)             # 路由服务监听端口
NETWORK_ROUTING_SERVER_NUM = config.get("NETWORK_ROUTING_SERVER_NUM", 5)    # 最大连接数
NETWORK_TIMEOUT_SECS = config.get("NETWORK_TIMEOUT_SECS", 2)                # 套接字操作的超时时间 float
