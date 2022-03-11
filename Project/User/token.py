# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/4 15:52
import functools
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from Common.yaml_method import YamlMethod
from flask_httpauth import HTTPBasicAuth
from Project.User.Database.user_database import User
from Project.User.Database.user_database import UserSchema
from flask import request, g

auth = HTTPBasicAuth()
SECRET_KEY = 'testing platform'

evn = YamlMethod().read_data('environment.yaml')['evn']


# 生成token, 有效时间为一周
def generate_auth_token(user_name, expiration=604800):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps({'user_name': user_name})


# 解析token
def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    # token正确
    try:
        data = s.loads(token)
        return data
    # token过期
    except SignatureExpired:
        return None
    # token错误
    except BadSignature:
        return None


# 验证token
def verify_token(token):
    dic = {}

    # 先验证token
    res = verify_auth_token(token)
    if res is not None:
        user_name = res['user_name']
    else:
        return False

    # 验证数据库用户信息
    user = User.query.filter_by(userName=user_name).first()
    user_schema = UserSchema()
    user_data = user_schema.dump(user)
    if len(user_data) == 0:
        return False

    g.user_name = user_name
    dic['username'] = user_data['userName']
    dic['res'] = True
    return dic


code = YamlMethod().read_data('code.yaml')['code']


# 验证token装饰器 -- 需要使用到token解析参数
def token_verify(func):
    @functools.wraps(func)
    def is_verify():

        # postman调用
        if evn == 'postman':
            token = request.args.get('token')
        else:
            # vue前端页面调用
            token = request.headers.get('X-Token')

        dic = {}
        res = verify_token(token)
        if res is not False:
            user_name = res['username']
        else:
            dic['code'] = code[4]
            dic['message'] = 'token失效'
            return dic
        result = func(user_name)
        return result

    return is_verify


# 验证token装饰器 -- 不需要使用到token解析参数
def before_request(func):
    @functools.wraps(func)
    def is_verify():

        # postman调用
        if evn == 'postman':
            token = request.args.get('token')
        else:
            # vue前端页面调用
            token = request.headers.get('X-Token')

        dic = {}
        res = verify_token(token)

        if res is False:
            dic['code'] = code[4]
            dic['message'] = 'token失效'
            return dic
        result = func()
        return result

    return is_verify
