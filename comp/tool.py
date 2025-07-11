import hashlib
import uuid
import os
# from tabulate import tabulate
import json,time,datetime,decimal,uuid


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

def unset(d, keys):
    for key in keys.split(","):
        if key in d:
            del d[key]
def rand():
    md5 = hashlib.md5()
    md5.update((str(uuid.uuid4()) + str(os.urandom(32))).encode('utf-8'))
    return md5.hexdigest()


def md5(s):
    md5 = hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest()

def now_time(fmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(fmt, time.localtime(time.time()))


def json_ret(code, msg=None, data=""):
    if msg is None:
        msg = error_text[code]
    if data is None:
        data = ""
    return {"code": code, "data":data, "msg": msg}

def merge_deep(a, b):
    for key, value in b.items():
        if key in a and isinstance(a[key], dict) and isinstance(value, dict):
            a[key] = merge_deep(a[key], value)
        else:
            a[key] = value
    return a

def tprint(ele, deep=0):
    if deep == 0:
        prev = '|-'
    else:
        prev = '|' + '    |'*deep + '-'
    if isinstance(ele, dict):
        for key, value in ele.items():
            if not isinstance(value, dict) \
                and not isinstance(value, list) \
                    and not isinstance(value, set) :
                print(prev + key+'='+str(value))
            else:
                print(prev + key + ' ' + str(type(value)) + ' ' + str(len(value)))
                tprint(value, deep+1)
    elif isinstance(ele, list) or isinstance(ele, set):
        for e in ele:
             print(prev +str(e))
    else:
        s = '    '*deep
        print(s+'='+str(ele))

error_text = {
    0: '操作成功',
    1: '参数错误',
    2: '数据保存失败，请重试',
    3: '缺少必要的参数',
    5: '两次输入密码不一致，请检查',
    6: '该手机号已注册，请直接登录',
    7: '错误的手机号和密码',
    8: '不识别的图片格式',
    9: '已有相同标题的文章存在',
    10: '请正确填写手机号',
    11: '上次发送的验证码尚未过期',
    12: '已存在相同数据',
    13: '未登录',
    14: '未授权',
    15: '数据配置错误，请联系管理员',
    16: '验证码错误',
    17: '接口错误'
}
