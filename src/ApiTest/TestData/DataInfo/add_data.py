# -*- coding: utf-8 -*-
# @Author  : Kevin
# @Time    : 2022/3/18 14:55

import time
from Common.mysql import db
from src.ApiTest.TestData.Database.data_database import TestData
from Common.yaml_method import YamlMethod


class AddData:
    """
    新增测试数据
    """

    @staticmethod
    def add_data(data_name, value, create_user):
        """
        新增测试数据
        :param data_name: 测试数据名称
        :param value: 测试数据
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        data = TestData.query.filter_by(data_name=data_name).first()
        if data is None:
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 将信息插入数据库
            new_data = TestData(data_name=data_name, data_value=value, create_time=create_time, create_user=create_user)
            db.session.add(new_data)
            db.session.commit()

            res = {
                'code': code[0],
                'message': 'success',
                'data': {}
            }
            return res
        else:
            res = {
                'code': code[1],
                'message': '参数名已存在',
                'data': {}
            }
            return res
