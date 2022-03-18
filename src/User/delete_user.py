# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/1/7 17:10

from Common.mysql import db
from src.User.Database.user_database import User
from Common.yaml_method import YamlMethod
from sqlalchemy.exc import SQLAlchemyError


class DeleteUser:
    """
    删除用户接口
    """

    @staticmethod
    def delete_user(username):
        """
        删除用户
        :param username: 用户名
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        user = User.query.filter_by(userName=username).first()

        if user is not None:

            try:
                db.session.delete(user)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                res = {
                    'code': code[5],
                    'data': [],
                    'message': '删除失败'
                }
                return res

            res = {
                'code': code[5],
                'data': [],
                'message': '删除成功'
            }
            return res

        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '用户不存在'
            }
            return res
