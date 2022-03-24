# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/24 17:15

import json
from Common.mysql import app
from flask import jsonify, request
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from src.ApiTest.ProjectConfig.ProjectModule.add_module import AddModule
from src.ApiTest.ProjectConfig.ProjectModule.update_module import UpdateModule
from src.ApiTest.ProjectConfig.ProjectModule.delete_module import DeleteModule
from src.ApiTest.ProjectConfig.ProjectModule.module_list import ModuleList

code = YamlMethod().read_data('code.yaml')['code']


@app.route('/module/add', methods=['POST'])
@token_verify
def add_module(create_user):
    """
    添加项目模块信息接口
    :param create_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    module_name = data['moduleName']
    project_name = data['projectName']

    # 校验参数
    if not all([module_name, create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交注册信息
    res = AddModule().add_module(module_name, project_name, create_user)
    return jsonify(res)


@app.route('/module/list', methods=['POST'])
@before_request
def module_list():
    """
    获取项目模块名称列表接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    page = data['page']
    limit = data['limit']
    module_name = data['moduleName']
    project_name = data['projectName']

    res = ModuleList().module_list(page, limit, module_name, project_name)
    return res


@app.route('/module/update', methods=['POST'])
@token_verify
def module_update(update_user):
    """
    更新项目模块信息接口
    :param update_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    module_id = data['id']
    module_name = data['moduleName']
    project_data = data['projectName']
    if '/' in project_data:
        project_data = data['projectName'].split('/')
        project_name = project_data[0]
    else:
        project_name = project_data

    # 校验参数
    if not all([module_name, update_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = UpdateModule().update_module(module_id, module_name, project_name, update_user)
    return res


@app.route('/module/delete', methods=['POST'])
@before_request
def module_delete():
    """
    删除项目模块信息接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    module_name = data['moduleName']

    res = DeleteModule().delete_module(module_name)
    return res
