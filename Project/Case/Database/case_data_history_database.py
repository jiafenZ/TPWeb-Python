# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/21 15:24

from Common.mysql import db, ma
from sqlalchemy.dialects.mysql import LONGTEXT


# 新建表case_data_history
class CaseDataHistory(db.Model):
    __tablename__ = 'case_data_history'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer)
    text = db.Column(LONGTEXT)
    case_name_id = db.Column(db.Integer)
    case_name = db.Column(db.String(255))
    is_delete = db.Column(db.String(64))
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))


class CaseDataHistorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CaseDataHistory

