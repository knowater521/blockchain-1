"""区块链的整体数据结构"""
# 区块中的序列从1开始计算
from .btc import Btc
from .trans_input import TransInput
from .trans_output import TransOutput
from .transaction import Transaction
from .block import Block
from .blockchain import BlockChain


__all__ = ["Btc", "TransInput", "TransOutput", "Transaction", "Block", "BlockChain", ]


"""
# BlockChain 类
[
    # Block 类
    {
        "index": 1,                         # 索引
        "pre_hash": "593080b6d7f739dcfc85fa455248d8d0dd567151e1fe3fe61c78ca2ca1b54ad8", # 前一个区块的hash
        "timestap": 1593234287.1745853,   	# 时间戳
        "randnum": 34.35435,                # 使区块满足某种条件的随机数
        "transactions": [                   # 交易数量有上限和下限，每个交易都保存为一个json字符串
    		# Transaction 类
            {								# 第一条交易包含新区块的交易和其它交易的所有交易费
                "inputs": [                                 # 交易的输入描述
    				# TransInput 类
                    {
                        "block": 1,                         # 第几个区块
                        "trans": 4,                         # 第几个交易
                        "output": 2                         # 第几个输出
                    },
                    # ......多个输入
                ],
                "outputs": [                                # 交易的输出描述
                  	# TransOutput 类
                    {
                       	# Btc 类
                        "btcs": "0.34",                     # 金额，用字符串以解决计算机的误差问题
                        "address": "fjwj34jr3kj5346j5464j",      # 指向的地址
                    },
                    # ...... 多个输出
                ],
                "pub_hex": "jfdkjfew8fuew89fuweufew8",      # 公钥
                "signed": "78f78ewfusdf"                    # 签名
            },
            # ...... 多笔交易
        ]           
    },
	# ... 多个区块
]
"""