# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/24 13:50

from Common.mysql import db, ma


# 新建表case_tag
class CaseTag(db.Model):
    __tablename__ = 'case_tag'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(255))
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))


class CaseTagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CaseTag
