# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/8 14:46

from Common.mysql import db, ma


# 新建表UrlConfig
class UrlConfig(db.Model):
    __tablename__ = 'url_config'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    configName = db.Column(db.String(64), unique=True, index=True)  # 索引
    projectId = db.Column(db.String(64))
    projectName = db.Column(db.String(255))
    environment = db.Column(db.String(64))
    base_url = db.Column(db.String(255))
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))
    update_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))


class UrlConfigSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UrlConfig
