# -*- coding: utf-8 -*-
# @Author  : Kevin
# @Time    : 2022/3/18 15:14

from src.ApiTest.TestData.Database.data_database import TestData, TestDataSchema
from Common.yaml_method import YamlMethod


class DataList:
    """
    获取测试数据列表接口
    """

    @staticmethod
    def data_list():
        """
        获取测试数据列表接口
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        data = TestData.query.all()
        info = []
        for i in data:
            data_schema = TestDataSchema()
            data_info = data_schema.dump(i)
            # 将单条数据库信息添加到info中
            info.append(data_info)

        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'projectList': info,
            }
        }

        return res
