"""
处理数据的发送和请求
请求得到的数据本质上是字符串，要处理后才能使用
发送过去的数据本质上也是字符串，通过解析后发送
"""
import traceback
from urllib import request, parse
from swap import json_to_dict, json_to_list, dict_to_json, list_to_json

def get_dict_from_url(url):
    """向url请求dict数据"""
    response = {}
    try:
        r = request.urlopen(url)
        code, html = r.getcode(), r.read().decode("utf-8")
        if code == 200:
            response = json_to_dict(html)
    except Exception as e:
        traceback.print_exc()
        print(e)
    return response

def get_list_from_url(url):
    """向url请求list数据"""
    response = []
    try:
        r = request.urlopen(url)
        code, html = r.getcode(), r.read().decode("utf-8")
        if code == 200:
            response = json_to_list(html)
    except Exception as e:
        traceback.print_exc()
        print(e)
    return response

def send_dict_to_url(url, dict_data):
    """向url发送dict数据(POST方式)，返回响应的字符串"""
    result = ""
    if isinstance(dict_data, dict):
        dicts = {
            "dict": dict_to_json(dict_data)
        }
        try:
            data = parse.urlencode(dicts).encode("utf-8")
            r = request.urlopen(url, data=data)
            if r.getcode() == 200:
                result = r.read().decode("utf-8")
        except Exception as e:
            traceback.print_exc()
            print(e)
    return result

def send_list_to_url(url, list_data):
    """向url发送list数据，返回响应的字符串"""
    result = ""
    if isinstance(list_data, list):
        dicts = {
            "list": list_to_json(list_data)
        }
        try:
            data = parse.urlencode(dicts).encode("utf-8")
            r = request.urlopen(url, data=data)
            if r.getcode() == 200:
                result = r.read().decode("utf-8")
        except Exception as e:
            traceback.print_exc()
            print(e)
    return result
