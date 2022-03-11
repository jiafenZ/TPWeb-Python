# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/3/5 13:42

from Common.mysql import db, ma
from sqlalchemy.dialects.mysql import LONGTEXT


# 新建表todo_list
class TodoList(db.Model):
    __tablename__ = 'todo_list'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(LONGTEXT)
    todo_date = db.Column(db.String(64))
    create_user = db.Column(db.String(64))
    create_time = db.Column(db.DATETIME)
    update_time = db.Column(db.DATETIME)


class TodoListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TodoList
