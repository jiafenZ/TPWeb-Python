# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/1/4 15:52
import functools
import json

from jose import jwt
from datetime import datetime, timedelta
from Common.yaml_method import YamlMethod
from src.User.Database.user_database import User
from src.User.Database.user_database import UserSchema
from flask import request, g

evn = YamlMethod().read_data('environment.yaml')['evn']
SECRET_KEY = 'testing platform' # 加密密钥即自定义随机字符串
ALGORITHM = "HS256"  # 加密算法HS256


def generate_auth_token(name, expires_delta=None):
    """
    # 生成token
    :param name: 保存到token的值
    :param expires_delta: 过期时间
    :return:
    """
    if expires_delta:
        # expire = datetime.utcnow() + expires_delta
        expire = datetime.now() + expires_delta

    else:
        # expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        # 设置过期时间:7天后
        expire = datetime.now() + timedelta(minutes=10080)
    to_encode = {"exp": expire, "sub": str(name)}

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_auth_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
        # 抛出自定义异常， 然后捕获统一响应
        return None


# 验证token
def verify_token(token):
    dic = {}

    # 先验证token
    res = verify_auth_token(token)
    if res is not None:
        dic_res = eval(res['sub'])
        user_name = dic_res['user_name']
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
