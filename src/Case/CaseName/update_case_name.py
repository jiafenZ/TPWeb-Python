# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/16 18:37

import time
from Common.mysql import db
from sqlalchemy.exc import SQLAlchemyError
from Common.yaml_method import YamlMethod
from src.Case.Database.case_name_database import CaseName
from src.Case.Database.case_data_database import CaseData


class UpdateCaseName:
    """
    修改用例名称信息接口
    """

    @staticmethod
    def update_case_name(case_name_id, case_name, update_user):
        """
        修改用例名称接口
        :param case_name_id: 测试用例名称ID
        :param case_name: 测试用例名称
        :param update_user: 更新人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        caseName = CaseName.query.filter_by(id=case_name_id).first()

        if caseName:
            caseName.case_name = case_name
            caseName.update_time = update_time
            caseName.update_user = update_user
            case_data = CaseData.query.filter_by(case_name_id=case_name_id).first()
            if case_data:
                case_data.case_name = case_name
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                res = {
                    'code': code[6],
                    'data': [],
                    'message': '用例名称更新失败'
                }
                return res

            res = {
                'code': code[0],
                'data': [],
                'message': '用例名称更新成功'
            }
            return res

        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '用例名称不存在'
            }
            return res
