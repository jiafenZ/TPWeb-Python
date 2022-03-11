# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/10 15:44

from Project.User.Database.user_database import User
from Project.User.Database.user_database import UserSchema
from Common.yaml_method import YamlMethod


class UserList:
    """
    获取用户列表接口
    """

    @staticmethod
    def user_list(page, limit, user_name):
        """
        获取用户列表接口
        :param page: 页码
        :param limit: 每页多少条数据
        :param user_name: 用户名
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        if user_name == '':
            data = User.query.filter().paginate(page, limit)
        else:
            data = User.query.filter_by(userName=user_name).paginate(page, limit)
        user_info = []
        for i in data.items:
            user_schema = UserSchema()
            user_data = user_schema.dump(i)
            # 移除登录密码
            user_data.pop('password')
            # 将单条用户信息添加到用户列表user_info中
            user_info.append(user_data)

        total = data.total
        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'userList': user_info,
                'total': total,
                'authority': 1
            }
        }

        return res
