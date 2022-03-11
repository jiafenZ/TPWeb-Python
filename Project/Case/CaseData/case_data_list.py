# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/19 15:21

from Common.yaml_method import YamlMethod
from Project.Case.Database.case_data_database import CaseData, CaseDataSchema
from Project.Case.Database.case_name_database import CaseName, CaseNameSchema


class CaseDataList:
    """
    获取用例列表接口
    """

    @staticmethod
    def case_data_list(case_name_id):
        """
        获取用例列表接口
        :param case_name_id: 用例名称ID
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']
        # 定义是否存在下级目录标志变量
        is_name = '0'

        # 查询数据库，校验用户名和密码
        case_data = CaseData.query.filter_by(case_name_id=case_name_id).first()
        case_schema = CaseDataSchema()
        data = case_schema.dump(case_data)

        if data:
            if data['text']:
                case_text = eval(data['text'])
            else:
                case_text = 'noData'
        else:
            # 查询该文章名称有没有下级目录
            name_data = CaseName.query.all()
            for i in name_data:
                case_name_schema = CaseNameSchema()
                case_name_data = case_name_schema.dump(i)
                if case_name_data['parent_id'] == case_name_id:
                    is_name = '1'
            case_text = 'noData'

        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'initJson': case_text,
                'is_name': is_name
            }
        }

        return res
