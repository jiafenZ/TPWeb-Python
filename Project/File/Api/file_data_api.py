# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/3/1 15:31

import json
from Common.mysql import app
from flask import jsonify, request
from Project.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from Project.File.FileData.add_file_data import AddFileData
from Project.File.FileData.get_file_data import GetFileData

code = YamlMethod().read_data('code.yaml')['code']
evn = YamlMethod().read_data('environment.yaml')['evn']


@app.route('/file_data/add', methods=['POST'])
@token_verify
def add_file_data(create_user):
    """
    新增文章
    :param create_user: 创建人
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    content = data['content']
    file_name_id = data['name_id']
    file_name = data['file_name']
    is_open = data['is_open']
    is_edit = data['is_edit']

    # 校验参数
    if not all([content, str(file_name_id), file_name, is_open, is_edit, create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交保存文章数据
    res = AddFileData().add_file_data(content, file_name_id, file_name, is_open, is_edit, create_user)
    return res


@app.route('/file_data/content', methods=['POST'])
@token_verify
def get_file_data(request_user):
    """
    获取文章内容接口
    :return:
    """

    if evn == 'vue':
        data = json.loads(str(request.data, 'utf-8'))
        file_name_id = data['name_id']
    else:
        file_name_id = int(request.form.get('name_id'))

    res = GetFileData().get_file_data(file_name_id, request_user)
    return res

