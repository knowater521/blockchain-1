"""
数据交换：
把python数据转换成json数据以发送
把json数据转换成python数据以处理

补充：
json在python中是str类型
"""
import json
import traceback

# 发送数据所用

def dict_to_json(mydict):
    """把字典变成str数据"""
    jsons = ""
    if isinstance(mydict, dict):
        try:
            jsons = json.dumps(mydict)
        except Exception as e:
            traceback.print_exc()
            print(e)
    return jsons.replace(" ", "")

def list_to_json(mylist):
    """把字典数组变成str数据"""
    jsons = ""
    if isinstance(mylist, list):
        try:
            jsons = json.dumps(mylist)
        except Exception as e:
            traceback.print_exc()
            print(e)
    return jsons.replace(" ", "")

# 接收数据所用

def json_to_dict(html):
    """把str数据变成字典"""
    dicts = {}
    if isinstance(html, str):
        try:
            tap = json.loads(html, encoding="utf-8")
            dicts.update(tap)
        except Exception as e:
            traceback.print_exc()
            print(e)
    return dicts

def json_to_list(html):
    """把str数据变成列表"""
    lists = []
    if isinstance(html, str):
        try:
            tap = json.loads(html, encoding="utf-8")
            lists.extend(tap)
        except Exception as e:
            traceback.print_exc()
            print(e)
    return lists
