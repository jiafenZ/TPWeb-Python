# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/16 18:37

from src.Case.Database.case_name_database import CaseName, CaseNameSchema
from Common.yaml_method import YamlMethod


class CaseNameTree:
    """
    获取用例名称,并转换成树形结构
    """

    @staticmethod
    def case_name_tree():
        """
        获取用例名称,并转换成树形结构口
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        data = CaseName.query.all()
        info = []
        max_id = 0
        for i in data:
            case_name_schema = CaseNameSchema()
            case_name_data = case_name_schema.dump(i)
            # 移出时间信息
            case_name_data.pop('update_user')
            case_name_data.pop('update_time')
            case_name_data.pop('create_time')
            case_name_data.pop('create_user')
            # 判断是否是最大id
            if case_name_data['id'] > max_id:
                max_id = case_name_data['id']
            # 将单条数据库信息添加到info中
            info.append(case_name_data)

        new = '[]'
        while len(info) > 0:
            for info_key in info:
                if info_key['parent_id'] == 0:
                    str_info_key = '"parent_id": %s,' % info_key['parent_id'] + '"case_name": "%s",' % info_key['case_name'] + '"id": %s,' % info_key['id'] + '"children": [],'
                    new = new[0] + '{' + str_info_key + '}' + ',' + new[1:]
                    info.remove(info_key)
                else:
                    if len(new) == 0:
                        pass
                    else:
                        target = ' %s,"children": [' % info_key['parent_id']
                        if target in new:
                            start = new.find(target)
                            end = start + len(target)
                            insert_str = '"parent_id": %s,' % info_key['parent_id'] + '"case_name": "%s",' % info_key['case_name'] + '"id": %s,' % info_key['id'] + '"children": [],'
                            new = new[0:end] + '{' + insert_str + '}' + ',' + new[end:]
                            info.remove(info_key)
                        else:
                            pass

        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'CaseNameTree': eval(new),
                'startId': max_id
            }
        }

        return res
