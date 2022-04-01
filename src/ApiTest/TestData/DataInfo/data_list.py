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
    def data_list(page, limit, data_name):
        """
        获取测试数据列表接口
        :param page: 页码
        :param limit: 每页多少条数据
        :param data_name: 参数名称
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        if data_name == '':
            data = TestData.query.filter().paginate(page, limit)
        else:
            data = TestData.query.filter_by(data_name=data_name).paginate(page, limit)
        info = []
        for i in data.items:
            data_schema = TestDataSchema()
            data_info = data_schema.dump(i)
            # 将单条数据库信息添加到info中
            info.append(data_info)

        total = data.total
        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'dataList': info,
                'total': total
            }
        }

        return res
