# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/28 11:59

from src.ApiTest.ApiInfo.Database.api_database import ApiInfo, ApiInfoSchema
from Common.yaml_method import YamlMethod


class GetApiInfo:
    """
    获取接口列表接口
    """

    @staticmethod
    def api_info(api_id):
        """
        获取单个接口信息
        :param api_id: 接口ID
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        api_info = ApiInfo.query.filter_by(id=api_id).first()
        user_schema = ApiInfoSchema()
        info = user_schema.dump(api_info)

        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'api_info': info
            }
        }

        return res
