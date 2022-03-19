# -*- coding: utf-8 -*-
# @Author  : Kevin
# @Time    : 2022/3/18 15:16

import time
from Common.mysql import db
from src.ApiTest.TestData.Database.data_database import TestData, TestDataSchema
from sqlalchemy.exc import SQLAlchemyError
from Common.yaml_method import YamlMethod


class UpdateData:
    """
    更新测试数据信息接口
    """

    @staticmethod
    def update_data(data_id, data_name, value, update_user):
        """
        更新测试数据信息接口
        :param data_id: 测试数据ID
        :param data_name: 测试数据名称
        :param value: 测试数据
        :param update_user: 更新人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        data = TestData.query.filter_by(id=data_id).first()

        if data:
            data_info = TestData.query.filter_by(data_name=data_name).all()
            info = []
            for i in data_info:
                data_schema = TestDataSchema()
                name = data_schema.dump(i)
                info.append(name)
            if len(info) < 2:
                data.data_name = data_name
                data.data_value = value
                data.update_time = update_time
                data.update_user = update_user

                try:
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    res = {
                        'code': code[6],
                        'data': [],
                        'message': '测试数据信息更新失败'
                    }
                    return res
                res = {
                    'code': code[0],
                    'data': [],
                    'message': '测试数据信息更新成功'
                }
                return res
            else:
                res = {
                    'code': code[1],
                    'data': [],
                    'message': '测试数据名已存在'
                }
                return res
        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '测试数据不存在'
            }
            return res
