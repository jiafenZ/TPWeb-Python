# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/18 13:29

from Common.mysql import db, ma


# 新建表test_data
class TestData(db.Model):
    __tablename__ = 'test_data'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    data_name = db.Column(db.String(64), unique=True, index=True)  # 索引
    data_value = db.Column(db.String(255))
    create_user = db.Column(db.String(64))
    create_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))
    update_time = db.Column(db.DATETIME)


class TestDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TestData
