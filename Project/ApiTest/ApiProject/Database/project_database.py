# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/25 16:17

from Common.mysql import db, ma


# 新建表Project
class Project(db.Model):
    __tablename__ = 'project'  # 数据库名称
    id = db.Column(db.Integer, primary_key=True)
    projectName = db.Column(db.String(64), unique=True, index=True)  # 索引
    describe = db.Column(db.String(255))
    create_time = db.Column(db.DATETIME)
    create_user = db.Column(db.String(64))
    update_time = db.Column(db.DATETIME)
    update_user = db.Column(db.String(64))


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
