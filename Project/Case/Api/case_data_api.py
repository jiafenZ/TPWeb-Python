# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/19 15:31

import json
from Common.mysql import app
from flask import jsonify, request
from Project.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from Project.Case.CaseData.add_case_data import AddCaseData
from Project.Case.CaseData.case_data_list import CaseDataList
from Project.Case.CaseData.case_tag_list import CaseTagList
from Project.Case.CaseData.add_sprint_case import AddSprintCase
from Project.Case.CaseData.sprint_case_count import SprintCaseCount

code = YamlMethod().read_data('code.yaml')['code']
evn = YamlMethod().read_data('environment.yaml')['evn']


@app.route('/case_data/add', methods=['POST'])
@token_verify
def add_case_data(create_user):
    """
    新增测试用例
    :param create_user: 创建人
    :return:
    """
    if evn == 'vue':
        data = json.loads(str(request.data, 'utf-8'))
        text = str(data['text'])
        case_name_id = data['name_id']
        case_name = data['case_name']
    else:
        text = request.form.get('text')
        case_name_id = int(request.form.get('name_id'))
        case_name = request.form.get('case_name')

    # 校验参数
    if not all([text, str(case_name_id), create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交保存测试用例数据
    res = AddCaseData().add_case_data(text, case_name_id, case_name, create_user)
    return res


@app.route('/case_data/list', methods=['POST'])
@before_request
def case_data_list():
    """
    获取测试用例列表接口
    :return:
    """

    if evn == 'vue':
        data = json.loads(str(request.data, 'utf-8'))
        case_name_id = data['case_name_id']
    else:
        case_name_id = int(request.form.get('case_name_id'))

    res = CaseDataList().case_data_list(case_name_id)
    return res


@app.route('/case_tag/list', methods=['POST'])
@before_request
def case_tag_list():
    """
    获取测试用例标签列表接口
    :return:
    """

    res = CaseTagList().case_tag_list()
    return res


@app.route('/sprint_case/add', methods=['POST'])
@token_verify
def add_sprint_case(create_user):
    """
    筛选版本测试用例接口
    :return:
    """

    data = json.loads(str(request.data, 'utf-8'))
    case_name_id = data['nameId']
    case_name = data['Name']
    name_id_list = data['submitCaseNameId']
    level_list = data['levelLabel']
    tag_list = data['submitCaselabel']

    # 校验参数
    if not all([str(case_name_id), case_name, name_id_list, create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    res = AddSprintCase().add_sprint_case(name_id_list, level_list, tag_list, case_name_id, case_name, create_user)
    return res


@app.route('/sprint_case/count', methods=['POST'])
@before_request
def sprint_case_count():
    """
    统计测试用例执行结果接口
    :return:
    """

    if evn == 'vue':
        data = json.loads(str(request.data, 'utf-8'))
        case_name_id = data['case_name_id']
    else:
        case_name_id = int(request.form.get('case_name_id'))

    res = SprintCaseCount().sprint_case_count(case_name_id)
    return res
