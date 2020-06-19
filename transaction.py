"""
交易的数据结构
对其的基本操作
交易中不能有相同的输入
"""
"""
dict类型：
{
    "inputs": [                                 # 交易的输入描述
        {
            "block": 0,                         # 第几个区块
            "trans": 4,                         # 第几个交易
            "export": 2                         # 第几个输出
        },
    ],
    "outputs": [                                # 交易的输出描述
        {
            "btcs": 0.34,                       # 金额
            "to": "fjwj34jr3kj5346j5464j",      # 指向的地址
            "valid": true                       # 有效性
        },
    ],
    "cost": 0.0004,                             # 交易费（打包成block后归0）
    "pub_key": "jfdkjfew8fuew89fuweufew8",      # 公钥
    "sign": "78f78ewfusdf"                      # 签名
}
"""
import traceback
from key import sign_key, verify_key, address_key
from swap import dict_to_json

class Transaction():
    """产生交易数据结构的模板"""
    def __init__(self):
        """产生一个交易模板"""
        self.input = []
        self.output = []
        self.cost = 0
        self.pub_key = ""
        self.sign = ""
    
    def add_input(self, block, trans, export):
        """向交易中添加输入"""
        input_dict = {}
        input_dict["block"] = int(block)
        input_dict["trans"] = int(trans)
        input_dict["export"] = int(export)
        self.input.append(input_dict)
    
    def add_output(self, btcs, to):
        """向交易中添加输出"""
        output_dict = {}
        output_dict["btcs"] = float(btcs)
        output_dict["to"] = str(to)
        output_dict["valid"] = True
        self.output.append(output_dict)

    def set_cost(self, cost):
        """设定交易费"""
        self.cost = float(cost)

    def sign_transaction(self, pub_str, pri_str):
        """对交易进行签名"""
        self.pub_key = pub_str
        tra_dict = self.derive_transaction()
        info = dict_to_json(tra_dict)
        sign = sign_key(info, pri_str)
        self.sign = sign

    def com_insum_outsum(self, chain_list):
        """算出交易的输入和输出的差"""
        trans_dict = self.derive_transaction()
        in_sum = 0
        for inp in trans_dict["inputs"]:
            utxo = get_trans_by_index(chain_list, inp["block"], inp["trans"], inp["export"])
            if utxo["valid"]:
                in_sum += utxo["btcs"]
        out_sum = trans_dict["cost"]
        for oup in trans_dict["outputs"]:
            if oup["valid"]:
                out_sum += oup["btcs"]
        return in_sum - out_sum
    
    def derive_transaction(self):
        """导出交易字典"""
        tra_dict = {
            "inputs": self.input,
            "outputs": self.output,
            "cost": self.cost,
            "pub_key": self.pub_key,
            "sign": self.sign
        }
        return tra_dict


def get_trans_by_index(chain_list, block_index, tras_index, output_index):
    """根据索引找到交易记录"""
    utxo = {}
    try:
        block = chain_list[block_index]
        tras = block["transactions"][tras_index]
        utxo = tras["outputs"][output_index]
    except Exception as e:
        traceback.print_exc()
        print(e)
    return utxo


def verify_transaction(chain_list, *trans_dicts):
    """验证一堆交易的有效性"""
    flag = False
    # copy一份
    trans_dict_list = []
    for trans_dict in trans_dicts:
        dicts = trans_dict.copy()
        trans_dict_list.append(dicts)
    # 验证签名
    for trans_dict in trans_dict_list:
        sign = trans_dict["sign"]
        trans_dict["sign"] = ""
        info = dict_to_json(trans_dict)
        pub_str = trans_dict["pub_key"]
        if not verify_key(info, sign, pub_str):
            return flag
    # 检查传入的交易中是否存在相同的输入
    for i, trans_dict in enumerate(trans_dict_list):
        inp_list1 = trans_dict["inputs"]
        for trans_dict_tap in trans_dict_list[i+1:]:
            inp_list2 = trans_dict_tap["inputs"]
            for inp_1 in inp_list1:
                for inp_2 in inp_list2:
                    if inp_1 == inp_2:
                        return flag
    # 验证输入和输出
    for trans_dict in trans_dict_list:
        pub_str = trans_dict["pub_key"]
        addr = address_key(pub_str)
        in_sum = 0
        for inp in trans_dict["inputs"]:
            utxo = get_trans_by_index(chain_list, inp["block"], inp["trans"], inp["export"])
            # 输入应为有效的输出，并且属于签名者
            if not utxo["valid"] or addr != utxo["to"]:
                return flag
            in_sum += utxo["btcs"]
        out_sum = trans_dict["cost"]
        for oup in trans_dict["outputs"]:
            # 输出应为有效的输出，并且交易费不能低于0
            if not oup["valid"] or oup["btcs"] <= 0:
                return flag
            out_sum += oup["btcs"]
        if in_sum != out_sum:
            return flag
    return True

def standard_transaction(trans_dict, pub_str):
    """规范化交易以打包成block"""
    cost = trans_dict["cost"]
    if cost > 0:
        trans_dict["cost"] = 0
        trans_dict["outputs"].append({
            "btcs": cost,
            "to": address_key(pub_str),
            "valid": True
        })
    return trans_dict

def un_standard_transaction(trans_dict):
    """把交易还原成规范化前以检查"""
    cost = trans_dict["outputs"][-1]["btcs"]
    trans_dict["cost"] = cost
    trans_dict["outputs"] = trans_dict["outputs"][:-1]
    return trans_dict

def create_reward_trans(pub_str):
    """生成一个矿工奖励的交易"""
    reward = {
        "inputs": [],
        "outputs": [
            {
                "btcs": 25,
                "to": address_key(pub_str),
                "valid": True
            }
        ],
        "cost": 0,
        "pub_key": pub_str,
        "sign": ""
    }
    return reward

def veri_reward_trans(trans_dict):
    """检查交易是否为合法的矿工交易"""
    if trans_dict["inputs"] == [] and trans_dict["cost"] == 0:
        if len(trans_dict["outputs"]) == 1 and trans_dict["outputs"][0]["btcs"] == 25:
            if trans_dict["outputs"][0]["valid"] == True:
                return True
    return False
