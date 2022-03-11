# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/7 11:15

from Common.mysql import db, ma


# 新建表MysqlConfig
class MysqlConfig(db.Model):
    __tablename__ = 'mysql_config'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    configName = db.Column(db.String(64), unique=True, index=True)  # 索引
    projectId = db.Column(db.String(64))
    projectName = db.Column(db.String(255))
    environment = db.Column(db.String(64))
    host = db.Column(db.String(255))
    port = db.Column(db.String(64))
    user = db.Column(db.String(255))
    password = db.Column(db.String(255))
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))
    update_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))


class MysqlConfigSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MysqlConfig
