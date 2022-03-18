# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/16 18:47

import json
from Common.mysql import app
from flask import jsonify, request
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from src.Case.CaseName.add_case_name import AddCaseName
from src.Case.CaseName.case_name_tree import CaseNameTree
from src.Case.CaseName.delete_case_name import DeleteCaseName
from src.Case.CaseName.update_case_name import UpdateCaseName
from src.Case.CaseName.case_name_list import CaseNameList

code = YamlMethod().read_data('code.yaml')['code']
evn = YamlMethod().read_data('environment.yaml')['evn']


@app.route('/case_name/add', methods=['POST'])
@token_verify
def add_case_name(create_user):
    """
    新增测试用例名称
    :param create_user: 创建人
    :return:
    """
    if evn == 'vue':
        data = json.loads(str(request.data, 'utf-8'))
        case_name = data['case_name']
        parent_id = data['parent_id']
    else:
        case_name = request.form.get('case_name')
        parent_id = request.form.get('parent_id')

    # 校验参数
    if not all([case_name, create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交注册信息
    res = AddCaseName().add_case_name(case_name, parent_id, create_user)
    return jsonify(res)


@app.route('/case_name/tree', methods=['POST'])
@before_request
def case_name_tree():
    """
    获取获取用例名称,并转换成树形结构接口
    :return:
    """

    res = CaseNameTree().case_name_tree()
    return res


@app.route('/case_name/list', methods=['POST'])
@before_request
def case_name_list():
    """
    获取获取用例名称列表接口
    :return:
    """

    res = CaseNameList().case_name_list()
    return res


@app.route('/case_name/delete', methods=['POST'])
@token_verify
def delete_case_name(create_user):
    """
    删除测试用例名称接口
    :param create_user: 删除人
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    case_name_id = data['id']

    res = DeleteCaseName().delete_case_name(case_name_id, create_user)
    return res


@app.route('/case_name/update', methods=['POST'])
@token_verify
def case_name_update(update_user):
    """
    更新测试用例名称接口
    :param update_user: 操作用户名
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    case_name_id = data['id']
    case_name = data['case_name']

    # 校验参数
    if not all([case_name_id, case_name, update_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = UpdateCaseName().update_case_name(case_name_id, case_name, update_user)
    return res
