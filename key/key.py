import rsa
from hashlib import sha256
from base64 import b64encode, b64decode
from typing import Optional, Tuple


class UserKey:
    """密钥类，用于管理公钥和私钥"""
    def __init__(self, pub_hex: str="", pri_hex: str="") -> None:
        """可以只创建pub_key或者只创建pri_key"""
        if pub_hex or pri_hex: # 创建key对象
            self.pub_key = self.hex_to_key(pub_hex, "pub")
            self.pri_key = self.hex_to_key(pri_hex, "pri")
        else:                   # 产生一个新key
            self.pub_key, self.pri_key = rsa.newkeys(512)

    @staticmethod
    def hex_to_key(key_hex: Optional[str], key_type: str) -> Optional[rsa.key.AbstractKey]:
        """把hex的key转换成obj"""
        if key_hex is None:
            return None
        result = None
        key_bytes = bytes.fromhex(key_hex)
        key_str = key_bytes.decode("utf-8")
        try:
            if key_type == "pub":
                result = rsa.PublicKey.load_pkcs1(key_bytes)
            elif key_type == "pri":
                result = rsa.PrivateKey.load_pkcs1(key_bytes)
        except Exception as e:
            print(e)
        return result

    def get_key_hex(self) -> Tuple[Optional[str], Optional[str]]:
        """导出hex形式的密钥"""
        return self.get_pub_hex(), self.get_pri_hex()

    def get_pub_hex(self) -> Optional[str]:
        """导出公钥"""
        if self.pub_key:
            return self.pub_key.save_pkcs1().hex()
        return None

    def get_pri_hex(self) -> Optional[str]:
        """导出私钥"""
        if self.pri_key:
            return self.pri_key.save_pkcs1().hex()
        return None

    def get_address(self) -> str:
        """导出address"""
        if self.pub_key is None:
            raise RuntimeError("public key is None!")
        pub_bytes = self.pub_key.save_pkcs1()
        addr = sha256(sha256(pub_bytes).digest()).hexdigest()
        return addr

    def sign(self, info: str) -> str:
        """对info内容进行签名"""
        if self.pri_key is None:
            raise RuntimeError("private key is None!")
        info_bytes = info.encode("utf-8")
        signed = rsa.sign(info_bytes, self.pri_key, "SHA-256")
        signed = b64encode(signed)
        return signed.hex()

    @classmethod
    def verify(cls, info: str, signed_hex: str, pub_hex: Optional[str]) -> bool:
        result = ""
        info_bytes = info.encode("utf-8")
        signed = b64decode(bytes.fromhex(signed_hex))
        pub_key = cls.hex_to_key(pub_hex, "pub")
        try:
            result = rsa.verify(info_bytes, signed, pub_key)
        except rsa.VerificationError as e:
            print(e)
        return result == "SHA-256"


if __name__ == "__main__":
    my_key = UserKey()
    print(my_key.get_address())
    print(my_key.get_key_hex())
    info = "艹，叼你妈的"
    sign_hex = my_key.sign(info)
    print(sign_hex)
    print(my_key.verify(info, sign_hex, my_key.get_pub_hex()))
