from flask import Flask, request, render_template
from swap import json_to_dict, list_to_json
from peer import Peer
from key import create_key
from block import create_first_block
from internet import get_dict_from_url

# 创世
p = Peer()
pub_key, pri_key = create_key()
keys = pub_key, pri_key

file = open("pub.key", "w")
file.write(pub_key)
file.close()
file = open("pri.key", "w")
file.write(pri_key)
file.close()

p.add_block(create_first_block(keys))
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """导航页"""
    return render_template("index.html")

@app.route("/transactions", methods=["POST"])
def get_trans():
    """接收其它节点发送的交易，合法则转发"""
    if request.method == "POST":
        s = request.form.get("dict")
        trans_dict = json_to_dict(s)
        if p.add_transaction(trans_dict):
            p.send_transaction(trans_dict)
            return "交易已添加"
    return "交易不合法"

@app.route("/blocks", methods=["POST"])
def get_block():
    """接收其它节点发送的区块，合法则转发"""
    if request.method == "POST":
        s = request.form.get("dict")
        block_dict = json_to_dict(s)
        if p.add_block(block_dict):
            p.send_block(block_dict)
            return "新的区块已添加"
    return "区块不合法"

@app.route("/blockchain", methods=["GET"])
def provide_chain():
    """提供完整的区块链"""
    chain_list = p.get_blockchain()
    ans = list_to_json(chain_list)
    return ans

@app.route("/trans_cache", methods=["GET"])
def provide_trans_cache():
    trans_list = p.get_trans_cache()
    ans = list_to_json(trans_list)
    return ans

@app.route("/friends", methods=["GET"])
def provide_friend():
    """提供自己连接的节点"""
    ip_list = p.get_friend_peer()
    ans = list_to_json(ip_list)
    return ans

@app.route("/mining", methods=["GET"])
def start_mining():
    """开始挖矿"""
    if p.get_trans_cache_height()>0:
        ip_list = p.get_friend_peer()
        for ip in ip_list:
            url = "http://" + ip + "/mining"
            get_dict_from_url(url)
        p.package_send_block(pub_key)
        return "挖矿完成"
    else:
        return "交易池中的交易数量不够"

if __name__ == "__main__":
    app.run(debug=True)
