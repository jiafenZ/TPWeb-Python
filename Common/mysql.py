# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2021/12/31 13:57
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'  # 密码
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@192.168.25.129:3306/tp_web'
"""
    协议：mysql+pymysql
    用户名：root
    密码：123456
    IP地址：192.168.21.139
    端口：3306
    数据库名：test #这里的数据库需要提前建好
"""


app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config["SQLALCHEMY_ECHO"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
