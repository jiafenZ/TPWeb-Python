# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2021/12/31 16:54

from flask import jsonify, request
from Common.mysql import app
import json
from src.User.register import Register
from src.User.login import Login
from src.User.logout import Logout
from src.User.user_info import UserInfo
from src.User.delete_user import DeleteUser
from src.User.update_user import UpdateUser
from src.User.user_list import UserList
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod


code = YamlMethod().read_data('code.yaml')['code']
evn = YamlMethod().read_data('environment.yaml')['evn']
debug = YamlMethod().read_data('environment.yaml')['debug']


@app.route('/user/register', methods=['POST'])
def register():
    """
    用户注册接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    user_name = data['username']
    password = data['password']
    real_name = data['realname']
    phone = data['phone']

    # 校验参数
    if not all([user_name, password, real_name, phone]):
        return jsonify(code=code[7], msg="注册信息不完整")

    # 提交注册信息
    res = Register().register(user_name, password, real_name, phone)
    return jsonify(res)


@app.route('/user/login', methods=['POST'])
def login():
    """
    后台登录接口
    :return:
    """
    if debug == 'vue':
        data = json.loads(str(request.data, 'utf-8'))
        user_name = data['username']
        password = data['password']
    else:
        user_name = request.form.get('username')
        password = request.form.get('password')

    # 校验参数
    if not all([user_name, password]):
        return jsonify(code=code[7], msg="登录信息不完整")

    res = Login().login(user_name, password)
    return jsonify(res)


@app.route('/user/logout', methods=['POST'])
def user_logout():
    """
    用户退出登录
    :return:
    """

    token = request.headers.get('X-Token')
    res = Logout().logout(token)
    return res


@app.route('/user/info', methods=['GET'])
@token_verify
def user_info(user_name):
    """
    获取用户信息接口
    :param user_name: 操作用户名
    :return:
    """

    res = UserInfo().user_info(user_name)
    return res


@app.route('/user/add', methods=['POST'])
@token_verify
def user_add(user):
    """
    新增用户接口
    :return:
    """
    roles = UserInfo().user_info(user)['data']['roles']
    if roles == 'admin':
        data = json.loads(str(request.data, 'utf-8'))
        user_name = data['userName']
        password = data['password']
        real_name = data['realName']
        phone = data['phone']
        roles = data['roles']
        status = data['status']

        # 校验参数
        if not all([user_name, password, real_name, phone]):
            return jsonify(code=code[7], msg="用户信息不完整")

        # 提交注册信息
        res = Register().register(user_name, password, real_name, phone, roles=roles, status=status)
    else:
        res = {
            'code': code[9],
            'data': {},
            'message': '您无操作权限'
        }
    return jsonify(res)


@app.route('/user/delete', methods=['POST'])
@before_request
def user_delete():
    """
    删除用户信息接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    user_name = data['userName']

    res = DeleteUser().delete_user(user_name)
    return res


@app.route('/user/update', methods=['POST'])
@token_verify
def user_update(user_name):
    """
    更新用户信息接口
    :param user_name: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    user_id = data['id']
    username = data['userName']
    password = data['password']
    real_name = data['realName']
    phone = data['phone']
    roles = data['roles']
    status = data['status']

    # 校验参数
    if not all([user_id, username, real_name, phone, roles, status]):
        return jsonify(code=code[7], msg="用户信息不完整")

    res = UpdateUser().update_user(user_id, username, password, real_name, phone, roles, status, user_name)
    return res


@app.route('/user/userList', methods=['POST'])
@token_verify
def user_list(user):
    """
    获取用户列表接口
    :param user: 操作用户名
    :return:
    """

    roles = UserInfo().user_info(user)['data']['roles']
    if roles == 'admin':
        data = json.loads(str(request.data, 'utf-8'))
        page = data['page']
        limit = data['limit']
        user_name = data['userName']
        res = UserList().user_list(page, limit, user_name)
    else:
        res = {
            'code': 20000,
            'data': {
                'userList': '',
                'total': '',
                'authority': 2
            },
            'message': '您无查看权限'
        }
    return res
