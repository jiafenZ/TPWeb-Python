# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/1 18:47

import json
from Common.mysql import app
from flask import jsonify, request
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from src.File.FileName.add_file_name import AddFileName
from src.File.FileName.file_name_tree import FileNameTree
from src.File.FileName.update_file_name import UpdateFileName
from src.File.FileName.delete_file_name import DeleteFileName

code = YamlMethod().read_data('code.yaml')['code']
evn = YamlMethod().read_data('environment.yaml')['evn']
debug = YamlMethod().read_data('environment.yaml')['debug']


@app.route('/file_name/add', methods=['POST'])
@token_verify
def add_file_name(create_user):
    """
    新增文章名称
    :param create_user: 创建人
    :return:
    """
    if debug == 'vue':
        data = json.loads(str(request.data, 'utf-8'))
        file_name = data['file_name']
        parent_id = data['parent_id']
    else:
        file_name = request.form.get('file_name')
        parent_id = request.form.get('parent_id')

    # 校验参数
    if not all([file_name, create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交注册信息
    res = AddFileName().add_file_name(file_name, parent_id, create_user)
    return jsonify(res)


@app.route('/file_name/tree', methods=['POST'])
@before_request
def file_name_tree():
    """
    获取获取文章名称,并转换成树形结构接口
    :return:
    """

    res = FileNameTree().file_name_tree()
    return res


@app.route('/file_name/delete', methods=['POST'])
@token_verify
def delete_file_name(create_user):
    """
    删除文章名称接口
    :param create_user: 删除人
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    file_name_id = data['id']

    res = DeleteFileName().delete_file_name(file_name_id, create_user)
    return res


@app.route('/file_name/update', methods=['POST'])
@token_verify
def file_name_update(update_user):
    """
    更新文章名称接口
    :param update_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    file_name_id = data['id']
    file_name = data['file_name']

    # 校验参数
    if not all([file_name_id, file_name, update_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = UpdateFileName().update_file_name(file_name_id, file_name, update_user)
    return res
