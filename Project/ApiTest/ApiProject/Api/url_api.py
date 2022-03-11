# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/8 15:01
import json
from Common.mysql import app
from flask import jsonify, request
from Project.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from Project.ApiTest.ApiProject.URLInfo.add_baseUrl import AddUrlInfo
from Project.ApiTest.ApiProject.URLInfo.baseUrl_list import UrlList
from Project.ApiTest.ApiProject.URLInfo.update_baseUrl import UpdateUrlInfo
from Project.ApiTest.ApiProject.URLInfo.delete_baseUrl import DeleteUrlInfo

code = YamlMethod().read_data('code.yaml')['code']


@app.route('/url/add', methods=['POST'])
@token_verify
def add_url(create_user):
    """
    添加url配置信息接口
    :param create_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    config_name = data['configName']
    project_data = data['projectName'].split('/')
    project_name = project_data[0]
    project_id = project_data[1]
    environment = data['environment']
    base_url = data['base_url']

    # 校验参数
    if not all([config_name, project_id, project_name, environment, base_url]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交注册信息
    res = AddUrlInfo().add_url_info(config_name, project_id, project_name, environment, base_url, create_user)
    return jsonify(res)


@app.route('/url/list', methods=['POST'])
@before_request
def url_list():
    """
    获取url配置列表接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    page = data['page']
    limit = data['limit']
    config_name = data['configName']
    project_name = data['projectName']

    res = UrlList().url_list(page, limit, config_name, project_name)
    return res


@app.route('/url/update', methods=['POST'])
@token_verify
def url_update(update_user):
    """
    更新url配置信息接口
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
    base_url = data['base_url']

    # 校验参数
    if not all([config_name, project_id, project_name, environment, base_url, update_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = UpdateUrlInfo().update_url_info(config_id, config_name, project_id, project_name, environment, base_url,
                                          update_user)
    return res


@app.route('/url/delete', methods=['POST'])
@before_request
def url_delete():
    """
    删除url配置信息接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    config_name = data['configName']

    res = DeleteUrlInfo().delete_url_info(config_name)
    return res
