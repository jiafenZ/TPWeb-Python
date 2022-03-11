# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/3/8 16:52

import time
from Common.yaml_method import YamlMethod
from Project.TodoList.Database.todo_list_database import TodoList, TodoListSchema


class GetTodoTag:
    """
    获取当月已添加待办事项日期接口
    """

    @staticmethod
    def get_todo_tag(request_user, date):
        """
        获取当月已添加待办事项日期接口
        :param request_user: 请求人
        :param date: 日期(年-月)
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']
        tag_list = []
        tag_dic = {}
        todo_len = 0

        # 查询数据库中的待办事项内容
        todo_data = TodoList.query.filter_by(create_user=request_user).all()

        if todo_data:
            for i in todo_data:
                todo_schema = TodoListSchema()
                info = todo_schema.dump(i)
                if str(info['todo_date'])[:7] == date:
                    # 判断是否是当月的待办事项
                    tag_dic['todo_data'] = info['todo_date']
                    options = eval(info['contents'])['Options']
                    checked_options = eval(info['contents'])['checkedOptions']

                    if len(options) == len(checked_options):
                        # 判断待办事项是否全部完成
                        tag_dic['tag'] = 0
                        tag_list.append(tag_dic)
                        tag_dic = {}
                    else:
                        tag_dic['tag'] = 1
                        tag_list.append(tag_dic)
                        tag_dic = {}
                today_time = time.strftime("%Y-%m-%d", time.localtime())
                if str(info['todo_date'])[:10] == str(today_time):
                    # 查询当天未完成待办事项
                    options = eval(info['contents'])['Options']
                    checked_options = eval(info['contents'])['checkedOptions']
                    todo_len = len(options) - len(checked_options)

            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'todoListTag': tag_list,
                    'todo_len': todo_len
                }
            }
        else:
            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'todoListTag': tag_list,
                    'todo_len': todo_len
                }
            }
        return res

