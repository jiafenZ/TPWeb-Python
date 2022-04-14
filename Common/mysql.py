# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2021/12/31 13:57
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from Common.yaml_method import YamlMethod


app = Flask(__name__)
evn = YamlMethod().read_data('environment.yaml')['evn']

account = YamlMethod().read_data('account_info.yaml')['mysql'][evn]

app.config['SECRET_KEY'] = account[3]  # 密码
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s:%s/%s' % (account[2], account[3], account[0],
                                                                            account[1], account[4])

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config["SQLALCHEMY_ECHO"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
