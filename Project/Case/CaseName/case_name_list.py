# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/24 13:35

from Project.Case.Database.case_name_database import CaseName, CaseNameSchema
from Common.yaml_method import YamlMethod


class CaseNameList:
    """
    获取用例名称列表接口
    """

    @staticmethod
    def case_name_list():
        """
        获取用例名称列表接口
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        data = CaseName.query.all()
        info = []
        for i in data:
            case_name_schema = CaseNameSchema()
            case_name_data = case_name_schema.dump(i)
            # 移出时间信息
            case_name_data.pop('update_user')
            case_name_data.pop('update_time')
            case_name_data.pop('create_time')
            case_name_data.pop('create_user')
            # 将单条数据库信息添加到info中
            case_name = {
                'value': case_name_data['id'],
                'label': case_name_data['case_name']
            }
            info.append(case_name)

        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'CaseNamelist': info,
            }
        }

        return res
