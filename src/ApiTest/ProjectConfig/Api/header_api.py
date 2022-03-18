# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/8 15:59
import json
from Common.mysql import app
from flask import jsonify, request
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from src.ApiTest.ProjectConfig.HeaderInfo.add_header import AddHeaderInfo
from src.ApiTest.ProjectConfig.HeaderInfo.header_list import HeaderList
from src.ApiTest.ProjectConfig.HeaderInfo.update_header import UpdateHeaderInfo
from src.ApiTest.ProjectConfig.HeaderInfo.delete_header import DeleteHeaderInfo

code = YamlMethod().read_data('code.yaml')['code']


@app.route('/header/add', methods=['POST'])
@token_verify
def add_header(create_user):
    """
    添加header配置信息接口
    :param create_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    config_name = data['configName']
    project_data = data['projectName'].split('/')
    project_name = project_data[0]
    project_id = project_data[1]
    environment = data['environment']
    header = data['header']

    # 校验参数
    if not all([config_name, project_id, project_name, environment, header]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交注册信息
    res = AddHeaderInfo().add_header_info(config_name, project_id, project_name, environment, header, create_user)
    return jsonify(res)


@app.route('/header/list', methods=['POST'])
@before_request
def header_list():
    """
    获取header配置列表接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    page = data['page']
    limit = data['limit']
    config_name = data['configName']
    project_name = data['projectName']

    res = HeaderList().header_list(page, limit, config_name, project_name)
    return res


@app.route('/header/update', methods=['POST'])
@token_verify
def header_update(update_user):
    """
    更新header配置信息接口
    :param update_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    config_id = data['id']
    config_name = data['configName']
    project_data = data['projectName']
    if '/' in project_data:
        project_data = data['projectName'].split('/')
        project_name = project_data[0]
        project_id = project_data[1]
    else:
        project_name = project_data
        project_id = data['projectId']
    environment = data['environment']
    header = data['header']

    # 校验参数
    if not all([config_name, project_id, project_name, environment, header, update_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = UpdateHeaderInfo().update_header_info(config_id, config_name, project_id, project_name, environment, header,
                                                update_user)
    return res


@app.route('/header/delete', methods=['POST'])
@before_request
def header_delete():
    """
    删除header配置信息接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    config_name = data['configName']

    res = DeleteHeaderInfo().delete_header_info(config_name)
    return res
