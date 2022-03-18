# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/16 18:36

import time
from Common.mysql import db
from Common.yaml_method import YamlMethod
from src.Case.Database.case_name_database import CaseName


class AddCaseName:
    """
    新增用例名称
    """
    @staticmethod
    def add_case_name(case_name, parent_id, create_user):
        """
        新增用例名称
        :param case_name: 用例名称
        :param parent_id: 用例父ID
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        data = CaseName(case_name=case_name, parent_id=parent_id, create_time=create_time, create_user=create_user)
        db.session.add(data)
        db.session.commit()

        res = {
            'code': code[0],
            'message': 'success',
            'data': {}
        }
        return res
