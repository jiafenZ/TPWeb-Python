# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/24 16:51

from Common.mysql import db, ma


# 新建表module
class Module(db.Model):
    __tablename__ = 'module'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    moduleName = db.Column(db.String(64), unique=True, index=True)  # 索引
    projectId = db.Column(db.String(64))
    projectName = db.Column(db.String(64))
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(65))
    update_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))


class ModuleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Module
