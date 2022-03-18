# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/16 18:27

from Common.mysql import db, ma


# 新建表case_name
class CaseName(db.Model):
    __tablename__ = 'case_name'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    case_name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer)
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))
    update_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))


class CaseNameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CaseName
