# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/4 15:48

import time
from Common.mysql import db
from Project.User.Database.user_database import User
from Common.public_method import md_5
from Project.User.Database.user_database import UserSchema
from Common.yaml_method import YamlMethod
from Project.User.token import generate_auth_token


class Login:
    """
    后台登录接口
    """

    @staticmethod
    def login(user_name, password):
        """
        登录接口
        :param user_name: 前端传过来的用户名
        :param password: 前端传过来的密码
        :return: 登录结果和用户信息
        """
        data = {}
        dic = {}

        code = YamlMethod().read_data('code.yaml')['code']

        # 查询数据库，校验用户名和密码
        user = User.query.filter_by(userName=user_name).first()
        user_schema = UserSchema()
        user_data = user_schema.dump(user)

        if len(user_data) != 0:
            # 判断账号是否被禁用
            if user_data['status'] != '启用':
                dic['code'] = code[8]
                dic['message'] = '账号被禁用，请联系管理员'
                return dic
            password = md_5(password)
            if user_data['password'] == password:
                dic['code'] = code[0]
                dic['message'] = '登录成功'

                # 生成token
                token = generate_auth_token(user_name)
                data['token'] = token.decode()

                # 记录登录时间
                login_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                user.lastLogin_time = login_time
                db.session.commit()

                # 返回角色和账号状态信息
                data['roles'] = [user_data['roles']]
                data['status'] = user_data['status']
                dic['data'] = data
                return dic
            else:
                dic['code'] = code[2]
                dic['message'] = '用户名或密码错误'
                return dic
        else:
            dic['code'] = code[3]
            dic['message'] = '用户不存在'
            return dic
