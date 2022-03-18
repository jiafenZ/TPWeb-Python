# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/1 15:24

from Common.mysql import db, ma
from sqlalchemy.dialects.mysql import LONGTEXT


# 新建表file_data_history
class FileDataHistory(db.Model):
    __tablename__ = 'file_data_history'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer)
    content = db.Column(LONGTEXT)
    file_name_id = db.Column(db.Integer)
    file_name = db.Column(db.String(255))
    is_open = db.Column(db.String(64))
    is_edit = db.Column(db.String(64))
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))


class FileDataHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FileDataHistory

