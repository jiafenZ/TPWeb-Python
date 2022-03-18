# -*- coding: utf-8 -*-
# @Author  : Kevin
# @Time    : 2022/3/18 15:44

import json
from Common.mysql import app
from flask import jsonify, request
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from src.ApiTest.TestData.DataInfo.add_data import AddData
from src.ApiTest.TestData.DataInfo.data_list import DataList
from src.ApiTest.TestData.DataInfo.updata_data import UpdateData
from src.ApiTest.TestData.DataInfo.delete_data import DeleteData

code = YamlMethod().read_data('code.yaml')['code']


@app.route('/data/add', methods=['POST'])
@token_verify
def add_data(create_user):
    """
    添加测试数据信息接口
    :param create_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    data_name = data['data_name']
    value = data['value']

    # 校验参数
    if not all([data_name, value, create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交注册信息
    res = AddData().add_data(data_name, value, create_user)
    return jsonify(res)


@app.route('/data/list', methods=['POST'])
@before_request
def data_list():
    """
    获取测试数据列表接口
    :return:
    """

    res = DataList().data_list()
    return res


@app.route('/data/update', methods=['POST'])
@token_verify
def update_data(update_user):
    """
    更新测试数据信息接口
    :param update_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    data_id = data['id']
    data_name = data['data_name']
    value = data['value']

    # 校验参数
    if not all([str(data_id), data_name, value, update_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = UpdateData().update_data(data_id, data_name, value, update_user)
    return res


@app.route('/data/delete', methods=['POST'])
@before_request
def delete_data():
    """
    删除测试数据信息接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    data_name = data['data_name']

    res = DeleteData().delete_data(data_name)
    return res
