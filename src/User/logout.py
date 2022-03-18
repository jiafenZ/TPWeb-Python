# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/1/6 11:32
from src.User.token import verify_token
from Common.yaml_method import YamlMethod


class Logout:
    """
    退出登录接口
    """

    @staticmethod
    def logout(token):
        """
        用户退出登录
        :param token: 前端请求头传过来的token
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        # 验证token
        res = verify_token(token)
        if res is not False:
            return {'code': code[0], 'data': 'success'}
        else:
            return {'code': code[4], 'data': 'token error'}
