"""交易的数据结构"""
"""
dict类型：
{
    "inputs": [                                 # 交易的输入描述
        {
            "block": 1,                         # 第几个区块
            "trans": 4,                         # 第几个交易
            "output": 2                         # 第几个输出
        },
    ],
    "outputs": [                                # 交易的输出描述
        {
            "btcs": 0.34,                       # 金额
            "address": "fjwj34jr3kj5346j5464j",      # 指向的地址
        },
    ],
    "pub_hex": "jfdkjfew8fuew89fuweufew8",      # 公钥
    "signed": "78f78ewfusdf"                    # 签名
}
交易费=输入-输出
"""
from typing import List, Any
import json

from key import UserKey
from .trans_input import TransInput
from .trans_output import TransOutput


__all__ = ["Transaction", ]


class Transaction:
    """管理单个交易的类"""
    def __init__(self, trans: str="") -> None:
        """初始化"""
        self.inputs: List[TransInput] = []         # 交易的输入
        self.outputs: List[TransOutput] = []        # 交易的输出
        self.pub_hex = ""       # 验证交易用的公钥
        self.signed = ""         # 签名
        if trans:
            self.load_trans(trans)
    
    def load_trans(self, trans: str) -> None:
        """根据json数据初始化trans"""
        trans_dict = json.loads(trans)
        input_list = trans_dict.get("inputs", [])
        if input_list:
            self.inputs = []
            for trans_input in input_list:
                self.inputs.append(TransInput(trans_input=trans_input))
        output_list = trans_dict.get("outputs", [])
        if output_list:
            self.outputs = []
            for trans_output in output_list:
                self.outputs.append(TransOutput(trans_output=trans_output))
        self.pub_hex = trans_dict.get("pub_hex", self.pub_hex)
        self.signed = trans_dict.get("signed", self.signed)

    def get_pub_key(self) -> UserKey:
        return UserKey(pub_hex=self.pub_hex)
    
    def get_signed(self) -> str:
        return self.signed

    def get_input(self, input: int) -> TransInput:
        """获取第input个输入"""
        return self.inputs[input - 1]

    def get_inputs(self) -> List[TransInput]:
        """获取全部输入"""
        return self.inputs

    def add_input(self, trans_input: TransInput) -> None:
        """向交易中添加输入"""
        self.inputs.append(trans_input)
    
    def get_output(self, output: int) -> TransOutput:
        """获取第output个输出"""
        return self.outputs[output - 1]

    def get_outputs(self) -> List[TransOutput]:
        """获取全部输出"""
        return self.outputs

    def compute_outputs_btcs(self) -> float:
        """计算一个交易中的输出总btc"""
        fee = 0.0
        for outp in self.get_outputs():
            fee += outp.btcs
        return fee

    def add_output(self, trans_output: TransOutput) -> None:
        """向交易中添加输出"""
        self.outputs.append(trans_output)

    def sign_transaction(self, user_key: UserKey) -> None:
        """对交易进行签名"""
        info = self.to_string_without_sign()
        pub = user_key.get_pub_hex()
        if pub is None:
            raise RuntimeError("public key is None!")
        self.pub_hex = pub
        self.signed = user_key.sign(info)

    def verify_transaction(self, user_key: UserKey=None) -> bool:
        """用公钥验证交易"""
        info = self.to_string_without_sign()
        if user_key is None:
            user_key = UserKey(pub_hex=self.pub_hex)
        return user_key.verify(info, self.signed, user_key.get_pub_hex())

    def keys(self) -> List[str]:
        return [
            "inputs",
            "outputs",
            "pub_hex",
            "signed"
        ]

    def __getitem__(self, key: str) -> Any:
        value = getattr(self, key)
        if key == "inputs" or key == "outputs":
            value = [str(tap) for tap in value]
        return value

    def to_string_without_sign(self) -> str:
        """导出字符串（不包含签名消息）"""
        trans_dict = dict(self)
        del trans_dict["pub_hex"]
        del trans_dict["signed"]
        return json.dumps(trans_dict).replace(" ", "")

    def __str__(self) -> str:
        """把本次交易转换成字符串"""
        return json.dumps(dict(self)).replace(" ", "")


if __name__ == "__main__":
    trans = Transaction()
    trans.add_input(TransInput(3, 5, 7))
    trans.add_output(TransOutput(5.67, "fsfwetewtette4654654"))
    key = UserKey()
    trans.sign_transaction(key)
    print(str(trans))
    print(trans.to_string_without_sign())
    trans2 = Transaction(trans=str(trans))
    print(trans2 == trans)
    print(trans2.verify_transaction(key))
    print(str(trans2) == str(trans))
