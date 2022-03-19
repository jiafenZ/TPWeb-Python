# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/1/10 11:13

import time
from Common.mysql import db
from src.User.Database.user_database import User, UserSchema
from Common.public_method import md_5
from sqlalchemy.exc import SQLAlchemyError
from Common.yaml_method import YamlMethod


class UpdateUser:
    """
    更新用户信息接口
    """

    @staticmethod
    def update_user(user_id, username, password, real_name, phone, roles, status, update_user):
        """
        更新用户信息接口
        :param user_id: 用户ID
        :param username: 登录账号
        :param password: 登录密码
        :param real_name: 真实姓名
        :param phone: 手机号码
        :param roles: 角色
        :param status: 账号状态
        :param update_user: 更新人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        user = User.query.filter_by(id=user_id).first()

        if user:
            # 查询是否存在相同登录账号名称
            name_info = User.query.filter_by(userName=username).first()
            user_schema = UserSchema()
            user_data = user_schema.dump(name_info)
            if user_data['id'] != user_id:
                res = {
                    'code': code[1],
                    'message': '登录账号名称已存在',
                    'data': {}
                }
                return res
            else:
                user.username = username
                user.realName = real_name
                user.phone = phone
                user.roles = roles
                user.status = status
                user.update_time = update_time
                user.update_user = update_user

                if password:
                    user.password = md_5(password)
                try:
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    res = {
                        'code': code[6],
                        'data': [],
                        'message': '更新用户信息失败'
                    }
                    return res

                res = {
                    'code': code[0],
                    'data': [],
                    'message': '更新用户信息成功'
                }
                return res
        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '用户不存在'
            }
            return res
