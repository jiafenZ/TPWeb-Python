# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2021/12/31 14:54

import time
from Common.mysql import db
from src.User.Database.user_database import User
from Common.public_method import md_5
from Common.yaml_method import YamlMethod


class Register:
    """
    后台注册接口
    """

    @staticmethod
    def register(user_name, password, real_name, phone, roles=None, status=None):
        """
        用户注册方法
        :param user_name: 登录用户名
        :param password: 登录密码
        :param real_name: 用户真实名称
        :param phone: 用户手机号码
        :param roles: 用户角色
        :param status: 账号状态
        :return:
        """
        code = YamlMethod().read_data('code.yaml')['code']

        # 查询用户名是否存在
        user = User.query.filter_by(userName=user_name).first()
        if user is None:
            md5_password = md_5(password)
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 默认用户新注册的角色为 editor
            if roles is None:
                roles = 'editor'
            if status is None:
                status = '启用'
            # 用户信息插入数据库
            user = User(userName=user_name, password=md5_password, realName=real_name, phone=phone, roles=roles,
                        create_time=create_time, status=status)
            db.session.add(user)
            db.session.commit()

            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'userName': user_name
                }
            }
            return res
        else:
            res = {
                'code': code[1],
                'message': '用户名已存在',
                'data': {}
            }
            return res
