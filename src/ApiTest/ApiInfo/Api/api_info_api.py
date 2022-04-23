# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/28 13:33

import json
from Common.mysql import app
from flask import jsonify, request
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from src.ApiTest.ApiInfo.info.add_aip import AddApi
from src.ApiTest.ApiInfo.info.update_api import UpdateApiInfo
from src.ApiTest.ApiInfo.info.delete_api import DeleteApi
from src.ApiTest.ApiInfo.info.api_list import ApiList
from src.ApiTest.ApiInfo.info.get_aip_info import GetApiInfo

code = YamlMethod().read_data('code.yaml')['code']


@app.route('/api/add', methods=['POST'])
@token_verify
def add_api(create_user):
    """
    添加接口信息接口
    :param create_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    api_name = data['apiName']
    project_name = data['projectName']
    module_name = data['moduleName']
    path = data['path']
    method = data['method']
    pre_parameter = data['pre_parameter']
    headers = data['headers']
    debug_headers = data['debug_headers']
    body = data['body']
    debug_body = data['debug_body']
    after_parameter = data['after_parameter']
    assert_sql = data['assert_sql']
    assert_parameter = data['assert_parameter']

    # 校验参数
    if not all([api_name, project_name, module_name, path, method, create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交信息
    res = AddApi().add_api(api_name, project_name, module_name, path, method, pre_parameter, headers, debug_headers, body,
                           debug_body, after_parameter, assert_sql, assert_parameter, create_user)
    return jsonify(res)


@app.route('/api/list', methods=['POST'])
@before_request
def api_list():
    """
    获取api列表接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    page = data['page']
    limit = data['limit']
    api_name = data['apiName']
    module_name = data['moduleName']
    project_name = data['projectName']

    res = ApiList().api_list(page, limit, api_name, module_name, project_name)
    return res


@app.route('/api/update', methods=['POST'])
@token_verify
def api_update(update_user):
    """
    更新api信息接口
    :param update_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))

    api_id = data['id']
    api_name = data['apiName']
    project_name = data['projectName']
    module_name = data['moduleName']
    path = data['path']
    method = data['method']
    pre_parameter = data['pre_parameter']
    headers = data['headers']
    debug_headers = data['debug_headers']
    body = data['body']
    debug_body = data['debug_body']
    after_parameter = data['after_parameter']
    assert_sql = data['assert_sql']
    assert_parameter = data['assert_parameter']

    # 校验参数
    if not all([api_id, api_name, project_name, module_name, path, method, update_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = UpdateApiInfo().update_api_info(api_id, api_name, project_name, module_name, path, method, pre_parameter,
                                          headers, debug_headers, body, debug_body, after_parameter, assert_sql,
                                          assert_parameter, update_user)
    return res


@app.route('/api/delete', methods=['POST'])
@before_request
def api_delete():
    """
    删除api信息接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    api_id = data['id']

    res = DeleteApi().delete_api(api_id)
    return res


@app.route('/api/info', methods=['POST'])
@before_request
def api_info():
    """
    获取单个Api信息接口
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    api_id = data['id']
    print(data)

    res = GetApiInfo().api_info(api_id)
    return res


