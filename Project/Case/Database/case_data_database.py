# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/19 15:10

from Common.mysql import db, ma
from sqlalchemy.dialects.mysql import LONGTEXT


# 新建表case_data
class CaseData(db.Model):
    __tablename__ = 'case_data'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(LONGTEXT)
    case_name_id = db.Column(db.Integer)
    case_name = db.Column(db.String(255))
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))
    update_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))


class CaseDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CaseData
