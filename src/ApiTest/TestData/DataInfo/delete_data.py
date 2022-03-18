# -*- coding: utf-8 -*-
# @Author  : Kevin
# @Time    : 2022/3/18 15:33

from Common.mysql import db
from src.ApiTest.TestData.Database.data_database import TestData
from Common.yaml_method import YamlMethod
from sqlalchemy.exc import SQLAlchemyError


class DeleteData:
    """
    删除测试数据接口
    """

    @staticmethod
    def delete_data(data_name):
        """
        删除测试数据信息
        :param data_name: 测试数据名称
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        data_info = TestData.query.filter_by(data_name=data_name).first()

        if data_info is not None:
            try:
                db.session.delete(data_info)
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
                'code': code[0],
                'data': [],
                'message': '删除成功'
            }
            return res

        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '测试数据不存在'
            }
            return res
