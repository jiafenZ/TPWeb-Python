# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/5 13:48

import time
from Common.mysql import db
from Common.yaml_method import YamlMethod
from src.TodoList.Database.todo_list_database import TodoList
from sqlalchemy.exc import SQLAlchemyError


class AddTodoList:
    """
    新增/编辑待办事项
    """
    @staticmethod
    def add_todo_list(todo_id, contents, todo_date, create_user):
        """
        新增/编辑待办事项
        :param todo_id: 待办事项内容ID
        :param contents: 待办事项内容
        :param todo_date: 待办日期
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 如果存在则更新数据
        if todo_id:
            todo = TodoList.query.filter_by(id=todo_id).first()
            # 更新todo_list数据
            todo.contents = contents
            todo.update_time = create_time
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
        # 如果不存在，则插入数据
        else:
            data = TodoList(contents=contents, todo_date=todo_date, create_user=create_user,
                            create_time=create_time)
            db.session.add(data)
            db.session.commit()

        res = {
            'code': code[0],
            'message': 'success',
            'data': {}
        }
        return res
