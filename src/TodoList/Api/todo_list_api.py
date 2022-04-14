# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/5 16:10

import json
from Common.mysql import app
from flask import jsonify, request
from src.User.token import token_verify, before_request
from Common.yaml_method import YamlMethod
from src.TodoList.TodoList.add_todo_list import AddTodoList
from src.TodoList.TodoList.get_todo_list import GetTodoList
from src.TodoList.TodoList.get_todo_tag import GetTodoTag


code = YamlMethod().read_data('code.yaml')['code']
evn = YamlMethod().read_data('environment.yaml')['evn']
debug = YamlMethod().read_data('environment.yaml')['debug']


@app.route('/todo_list/add', methods=['POST'])
@token_verify
def add_todo_list(create_user):
    """
    新增/编辑Todolist
    :param create_user: 创建人
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    contents = str(data['contents'])
    todo_date = data['todo_date']
    todo_id = data['todo_id']

    # 校验参数
    if not all([contents, todo_date, create_user]):
        return jsonify(code=code[7], msg="信息不完整")

    # 提交保存测试用例数据
    res = AddTodoList.add_todo_list(todo_id, contents, todo_date, create_user)
    return res


@app.route('/todo_list/get', methods=['POST'])
@token_verify
def get_todo_list(create_user):
    """
    获取Todolist内容
    :param create_user: 创建人
    :return:
    """
    if debug == 'vue':
        data = json.loads(str(request.data, 'utf-8'))
        todo_date = data['todo_date']
    else:
        todo_date = request.form.get('todo_date')

    res = GetTodoList().get_todo_list(create_user, todo_date)

    return res


@app.route('/todo_list/tag', methods=['POST'])
@token_verify
def get_todo_tag(create_user):
    """
    获取当月已添加待办事项日期接口
    :param create_user: 创建人
    :return:
    """
    data = json.loads(str(request.data, 'utf-8'))
    date = data['date']

    res = GetTodoTag().get_todo_tag(create_user, date)

    return res
