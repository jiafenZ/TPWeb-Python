# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/5 15:55
from Project.User.Database.user_database import User
from Project.User.Database.user_database import UserSchema
from Common.yaml_method import YamlMethod


class UserInfo:
    """
    获取用户信息接口
    """

    @staticmethod
    def user_info(user_name):
        """
        获取用户信息接口
        :param user_name: 用户名
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        dic = {}

        user = User.query.filter_by(userName=user_name).first()
        user_schema = UserSchema()
        user_data = user_schema.dump(user)

        user_info = {
            'userName': user_data['userName'],
            'realName': user_data['realName'],
            'roles': user_data['roles'],
            'status': user_data['status']
        }

        dic['code'] = code[0]
        dic['data'] = user_info
        return dic
