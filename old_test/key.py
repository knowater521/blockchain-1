"""
对公钥和私钥的管理和操作
公钥、私钥均被编码为16进制表示的字符串
钱包地址由公钥直接算出
私钥对消息进行签名操作，公钥可以验证某字符串是否是其所签
"""
"""
公钥：
-----BEGIN RSA PUBLIC KEY-----
...
-----END RSA PUBLIC KEY-----
私钥：
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
"""
import rsa
import base64
import hashlib
import re
import traceback

__all__ = ["create_key", "sign_key", "verify_key", "address_key"]

def encode_key(key_obj):
    """对密钥进行编码"""
    result = ""
    if isinstance(key_obj, (rsa.PublicKey, rsa.PrivateKey)):
        key_bytes = key_obj.save_pkcs1()
        # key_str = key_bytes.decode("utf-8")
        # key_str = re.sub("\s*?-----.*?KEY-----\s*?", "", key_str)
        # key_bytes = key_str.encode("utf-8")
        result = key_bytes.hex()
    return result

def decode_key(key_str):
    """对密钥进行译码"""
    result = None
    if isinstance(key_str, str):
        key_str = key_str.strip()
        try:
            key_bytes = bytes.fromhex(key_str)
            key_str = key_bytes.decode("utf-8")
            if re.match("-----BEGIN RSA PUBLIC KEY-----.*?-----END RSA PUBLIC KEY-----", key_str, re.S):
                result = rsa.PublicKey.load_pkcs1(key_bytes)
            elif re.match("-----BEGIN RSA PRIVATE KEY-----.*?-----END RSA PRIVATE KEY-----", key_str, re.S):
                result = rsa.PrivateKey.load_pkcs1(key_bytes)
        except Exception as e:
            traceback.print_exc()
            print(e)
    return result

def create_key():
    """产生新的密钥对"""
    pub_key, pri_key = rsa.newkeys(512)
    pub_str, pri_str = encode_key(pub_key), encode_key(pri_key)
    return pub_str, pri_str

def sign_key(info, pri_str):
    """用私钥对info内容进行数字签名"""
    sign = ""
    pri_key = decode_key(pri_str)
    info_bytes = info.encode("utf-8")
    if isinstance(pri_key, rsa.PrivateKey):
        signed = rsa.sign(info_bytes, pri_key, "SHA-256")
        signed = base64.b64encode(signed)
        sign = signed.hex()
    return sign

def verify_key(info, sign, pub_str):
    """用公钥验证info的数字签名"""
    result = ""
    info_bytes = info.encode("utf-8")
    signed = bytes.fromhex(sign)
    signed = base64.b64decode(signed)
    pub_key = decode_key(pub_str)
    if isinstance(pub_key, rsa.PublicKey):
        try:
            result = rsa.verify(info_bytes, signed, pub_key)
        except rsa.VerificationError as e:
            traceback.print_exc()
            print(e)
    return result == "SHA-256"

def address_key(pub_str):
    """根据公钥获取64位的钱包地址"""
    pub_bytes = bytes.fromhex(pub_str)
    addr = hashlib.sha256(pub_bytes).hexdigest()
    return addr
