# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2021/12/31 14:29

from Common.mysql import db, ma


# 新建表User
class User(db.Model):
    __tablename__ = 'user'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64), unique=True, index=True)  # 索引
    password = db.Column(db.String(64))
    realName = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    roles = db.Column(db.String(32))
    status = db.Column(db.String(32))
    lastLogin_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))
    update_time = db.Column(db.DATETIME)
    create_time = db.Column(db.DATETIME)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
