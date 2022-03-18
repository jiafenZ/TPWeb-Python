# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/24 15:00

from src.Case.Database.case_tag_database import CaseTag, CaseTagSchema
from Common.yaml_method import YamlMethod


class CaseTagList:
    """
    获取用例标签列表接口
    """

    @staticmethod
    def case_tag_list():
        """
        获取用例标签列表接口
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        # 查询数据库，校验用户名和密码
        tag_data = CaseTag.query.filter_by(id=1).first()
        if tag_data:
            case_schema = CaseTagSchema()
            data = case_schema.dump(tag_data)
            tag_list_data = eval(data['tag'])['tag']
            info = []
            for value in tag_list_data:
                tag_list = {
                    'value': value,
                    'label': value
                }
                info.append(tag_list)

            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'tag': info
                }
            }
            return res
        else:
            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'tag': []
                }
            }

            return res
