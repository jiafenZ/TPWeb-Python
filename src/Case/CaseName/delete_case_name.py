# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/16 18:36

import time
from Common.mysql import db
from Common.yaml_method import YamlMethod
from sqlalchemy.exc import SQLAlchemyError
from src.Case.Database.case_data_database import CaseData, CaseDataSchema
from src.Case.Database.case_name_database import CaseName, CaseNameSchema
from src.Case.Database.case_data_history_database import CaseDataHistory


class DeleteCaseName:
    """
    删除测试用例名称
    """

    @staticmethod
    def delete_case_name(case_name_id, create_user):
        """
        删除测试用例名称
        :param case_name_id: 测试用例名称ID
        :param create_user: 删除人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        case_name_data = CaseName.query.filter_by(id=case_name_id).first()
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if case_name_data:
            case_data = CaseData.query.filter_by(case_name_id=case_name_id).first()
            if case_data:
                data_schema = CaseDataSchema()
                old_data = data_schema.dump(case_data)
                # 将表中的旧数据迁移到case_data_history表中
                case_id = old_data['id']
                text = old_data['text']
                case_name_id = old_data['case_name_id']
                case_name = old_data['case_name']
                data = CaseDataHistory(case_id=case_id, text=text, case_name_id=case_name_id, case_name=case_name,
                                       is_delete=1, create_time=create_time, create_user=create_user)
                db.session.add(data)
                db.session.commit()
                # 删除测试用例
                try:
                    db.session.delete(case_data)
                    db.session.commit()
                except SQLAlchemyError as e:
                    db.session.rollback()
                    res = {
                        'code': code[5],
                        'data': [],
                        'message': '删除测试用例失败'
                    }
                    return res
            # 删除用例名称
            try:
                db.session.delete(case_name_data)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                res = {
                    'code': code[5],
                    'data': [],
                    'message': '删除失败'
                }
                return res

            res = {
                'code': code[0],
                'data': [],
                'message': '删除成功'
            }
            return res

        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '测试用例名称不存在'
            }
            return res
