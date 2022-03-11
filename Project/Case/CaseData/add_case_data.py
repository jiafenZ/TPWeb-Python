# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/19 15:21

import re
import time
from Common.mysql import db
from Common.yaml_method import YamlMethod
from Project.Case.Database.case_data_database import CaseData, CaseDataSchema
from Project.Case.Database.case_data_history_database import CaseDataHistory
from Project.Case.Database.case_tag_database import CaseTag, CaseTagSchema
from sqlalchemy.exc import SQLAlchemyError


class AddCaseData:
    """
    新增测试用例
    """
    @staticmethod
    def insert_tag(text):
        """
        将测试用例中的自定义标签取出来，并插入标签库
        :param text: 测试用例中的text
        :return:
        """
        # 从text中取出自定义标签
        str_dic = str(text)
        str_list = str_dic.split("'resource': [")
        tag_list = []
        for resource in str_list[1:]:
            # 删除引号和空字符
            str_data = re.sub("'", "", resource.split("]")[0].replace(" ", ""))
            # 分割，组合成自定义标签tag列表
            data_list = str_data.split(",")
            tag_list = list(set(tag_list + data_list))
        # 查询tag表中的数据
        tag_data = CaseTag.query.filter_by(id=1).first()
        if tag_data:
            tag_schema = CaseTagSchema()
            old_tag = tag_schema.dump(tag_data)
            new_tag_data = list(set(eval(old_tag['tag'])['tag'] + tag_list))
            new_tag = {
                'tag': new_tag_data
            }
            # 插入新tag数据
            tag_data.tag = str(new_tag)
        else:
            new_tag_data = {
                'tag': tag_list
            }
            new_tag = CaseTag(tag=str(new_tag_data))
            db.session.add(new_tag)
            db.session.commit()

    def add_case_data(self, text, case_name_id, case_name, create_user):
        """
        新增测试用例
        :param text: 测试用例内容
        :param case_name_id: 用例名称ID
        :param case_name: 用例名称
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 查询数据库中该用例是否存在
        case_data = CaseData.query.filter_by(case_name_id=case_name_id).first()

        # 如果存在则进行数据迁移并更新数据
        if case_data:
            case_schema = CaseDataSchema()
            old_data = case_schema.dump(case_data)
            # 将表中的旧数据迁移到case_data_history表中
            case_id = old_data['id']
            old_text = old_data['text']
            case_name_id = old_data['case_name_id']
            case_name = old_data['case_name']
            data = CaseDataHistory(case_id=case_id, text=old_text, case_name_id=case_name_id, case_name=case_name,
                                   create_time=create_time, create_user=create_user)
            db.session.add(data)
            db.session.commit()
            # 更新case_data数据
            case_data.text = text
            case_data.update_time = create_time
            case_data.update_user = create_user
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
            # 从text中取出自定义标签，并插入数据库
            self.insert_tag(text)
        # 如果不存在，则插入数据
        else:
            data = CaseData(text=text, case_name_id=case_name_id, case_name=case_name, create_time=create_time,
                            create_user=create_user)
            db.session.add(data)
            db.session.commit()
            # 从text中取出自定义标签，并插入数据库
            self.insert_tag(text)

        res = {
            'code': code[0],
            'message': 'success',
            'data': {}
        }
        return res
