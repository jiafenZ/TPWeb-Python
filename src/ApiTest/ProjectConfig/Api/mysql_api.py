# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/7 13:32
import json
from Common.mysql import app
from flask import jsonify, request
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from src.ApiTest.ProjectConfig.MysqlInfo.add_mysqlinfo import AddMysqlInfo
from src.ApiTest.ProjectConfig.MysqlInfo.mysqlinfo_list import MysqlList
from src.ApiTest.ProjectConfig.MysqlInfo.update_mysqlinfo import UpdateMysqlInfo
from src.ApiTest.ProjectConfig.MysqlInfo.delete_mysqlinfo import DeleteMysqlInfo

code = YamlMethod().read_data('code.yaml')['code']


@app.route('/mysql/add', methods=['POST'])
@token_verify
def add_mysql(create_user):
    """
    添加数据库配置信息接口
    :param create_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
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
    host = data['host']
    port = data['port']
    user = data['user']
    password = data['password']

    # 校验参数
    if not all([config_name, project_id, project_name, environment, host, port, user, password]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交注册信息
    res = AddMysqlInfo().add_mysql_info(config_name, project_id, project_name, environment, host, port, user, password, create_user)
    return jsonify(res)


@app.route('/mysql/list', methods=['POST'])
@before_request
def mysql_list():
    """
    获取数据库配置列表接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    page = data['page']
    limit = data['limit']
    config_name = data['configName']
    project_name = data['projectName']

    res = MysqlList().mysql_list(page, limit, config_name, project_name)
    return res


@app.route('/mysql/update', methods=['POST'])
@token_verify
def mysql_update(update_user):
    """
    更新数据库配置信息接口
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
    host = data['host']
    port = data['port']
    user = data['user']
    password = data['password']

    # 校验参数
    if not all([config_name, project_id, project_name, environment, host, port, user, password, update_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = UpdateMysqlInfo().update_mysql_info(config_id, config_name, project_id, project_name, environment, host, port,
                                              user, password, update_user)
    return res


@app.route('/mysql/delete', methods=['POST'])
@before_request
def mysql_delete():
    """
    删除数据库配置信息接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    config_name = data['configName']

    res = DeleteMysqlInfo().delete_mysql_info(config_name)
    return res

