# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/1/25 16:30

import json
from Common.mysql import app
from flask import jsonify, request
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from src.ApiTest.ProjectInfo.info.add_project import AddProject
from src.ApiTest.ProjectInfo.info.project_list import ProjectList
from src.ApiTest.ProjectInfo.info.update_project import UpdateProject
from src.ApiTest.ProjectInfo.info.delete_project import DeleteProject

code = YamlMethod().read_data('code.yaml')['code']


@app.route('/project/add', methods=['POST'])
@token_verify
def add_project(create_user):
    """
    添加项目信息接口
    :param create_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    project_name = data['projectName']
    describe = data['describe']

    # project_name = request.form.get('projectName')
    # describe = request.form.get('describe')

    # 校验参数
    if not all([project_name, create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交信息
    res = AddProject().add_project(project_name, describe, create_user)
    return jsonify(res)


@app.route('/project/list', methods=['POST'])
@before_request
def project_list():
    """
    获取项目名称列表接口
    :return:
    """

    res = ProjectList().project_list()
    return res


@app.route('/project/update', methods=['POST'])
@token_verify
def project_update(update_user):
    """
    更新项目信息接口
    :param update_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    project_id = data['id']
    project_name = data['projectName']
    describe = data['describe']

    # 校验参数
    if not all([project_name, update_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = UpdateProject().update_project(project_id, project_name, describe, update_user)
    return res


@app.route('/project/delete', methods=['POST'])
@before_request
def project_delete():
    """
    删除项目信息接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    project_name = data['projectName']

    res = DeleteProject().delete_project(project_name)
    return res
