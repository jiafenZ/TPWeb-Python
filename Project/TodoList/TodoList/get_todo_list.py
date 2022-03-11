# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/3/5 14:05

import datetime
from Common.yaml_method import YamlMethod
from Project.TodoList.Database.todo_list_database import TodoList, TodoListSchema


class GetTodoList:
    """
    获取单日待办事项内容接口
    """

    @staticmethod
    def get_todo_list(request_user, todo_date):
        """
        获取单日待办事项内容接口
        :param request_user: 请求人
        :param todo_date: 待办日期
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        # 查询数据库中的待办事项内容
        date = datetime.datetime.strptime(todo_date+' 00:00:00', '%Y-%m-%d %H:%M:%S')
        todo_data = TodoList.query.filter_by(create_user=request_user, todo_date=date).first()
        if todo_data:
            todo_schema = TodoListSchema()
            info = todo_schema.dump(todo_data)
            contents = eval(info['contents'])

            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'Options': contents['Options'],
                    'checkedOptions': contents['checkedOptions'],
                    'todo_data': info['todo_date'],
                    'todo_id': info['id']
                }
            }
        else:
            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'Options': [],
                    'checkedOptions': [],
                    'todo_data': todo_date,
                    'todo_id': ''
                }
            }
        return res
