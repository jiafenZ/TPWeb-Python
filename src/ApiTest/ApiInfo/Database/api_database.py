# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/28 11:21

from Common.mysql import db, ma


# 新建表api_info
class ApiInfo(db.Model):
    __tablename__ = 'api_info'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    apiName = db.Column(db.String(64))
    projectName = db.Column(db.String(64))
    moduleName = db.Column(db.String(64))
    path = db.Column(db.String(255))
    method = db.Column(db.String(64))
    pre_parameter = db.Column(db.String(255))
    headers = db.Column(db.String(255))
    debug_headers = db.Column(db.String(255))
    body = db.Column(db.String(255))
    debug_body = db.Column(db.String(255))
    after_parameter = db.Column(db.String(255))
    assert_sql = db.Column(db.String(255))
    assert_parameter = db.Column(db.String(255))
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))
    update_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))


class ApiInfoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ApiInfo
