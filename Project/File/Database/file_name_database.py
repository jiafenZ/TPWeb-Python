# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/3/1 11:25

from Common.mysql import db, ma


# 新建表file_name
class FileName(db.Model):
    __tablename__ = 'file_name'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer)
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))
    update_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))


class FileNameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FileName
