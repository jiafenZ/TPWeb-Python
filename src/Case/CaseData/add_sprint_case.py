# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/22 17:55

import time
from Common.mysql import db
from Common.yaml_method import YamlMethod
from src.Case.Database.case_data_database import CaseData, CaseDataSchema
from src.Case.Database.case_data_history_database import CaseDataHistory
from sqlalchemy.exc import SQLAlchemyError


class Traverse:
    """
    遍历字典嵌套列表数据，并删除指定数据
    """

    str_dic = ''
    tag_list = [0]

    @staticmethod
    def str_key(key_list, str_data):
        """
        遍历字符串，判断是否存在目标字符串
        :param key_list: 给定的目标字符串列表
        :param str_data: 遍历的字符串
        :return: 如果存在任何一个目标字符串，则返回tag 1，反之则返回tag 0
        """
        tag = 0
        for key in key_list:
            if key in str_data:
                tag = 1
        return tag

    def new(self, key_list, data):
        """
        遍历字符串，并删除符合条件的目标字符串
        :param key_list: 给定的目标字符串列表
        :param data: 遍历的数据
        :return: 新的数据（字典嵌套列表）
        """
        # 如果字典中的 data 字段中没有目标字符串，则继续往下遍历，有则停止
        if self.str_key(key_list, str(data['data'])) == 0:
            # 如果字段中 children 字段为空列表，则删除字典中该元素（data 和 children 一起删除）
            if not data['children']:
                self.tag_list.append(0)
                if str(data) + ', ' in self.str_dic:
                    self.str_dic = self.str_dic.replace(str(data) + ', ', '')
                elif str(data) + ',' in self.str_dic:
                    self.str_dic = self.str_dic.replace(str(data) + ',', '')
                elif str(data) in self.str_dic:
                    # 空列表中最后一个元素没有逗号‘,’的处理
                    self.str_dic = self.str_dic.replace(str(data), '')
            else:
                # 如果字段中 children 字段不为空列表，则继续往下遍历列表中的每一个嵌套的字典元素
                for children in data['children']:
                    self.new(key_list, children)

    def new_data(self, key_list, dic):
        # 赋值元素数据字符串格式
        self.str_dic = str(dic)
        # 定义遍历标志列表
        self.tag_list.append(0)
        while self.tag_list:
            self.tag_list.clear()
            self.new(key_list, eval(self.str_dic))
        if self.str_dic != '':
            return eval(self.str_dic)
        else:
            return {}


class AddSprintCase:
    """
    筛选版本测试用例接口
    """

    @staticmethod
    def add_sprint_case(name_id_list, tag_list, level_list, case_name_id, case_name, create_user):
        """
        筛选版本测试用例接口
        :param name_id_list: 用例名称ID列表
        :param tag_list: 标签列表
        :param level_list: 用例等级列表
        :param case_name_id: 用例名称ID
        :param case_name: 用例名称
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        key_list = tag_list + level_list

        # 查询指定用例名称id的测试用例数据
        case_data = CaseData.query.filter(CaseData.case_name_id.in_(name_id_list)).all()
        if case_data:
            data_text = {'root': {'data': {'id': '1', 'created': 1645430786192, 'text': '测试用例'}, 'children': []},
                         'template': 'default', 'theme': 'fresh-green', 'version': '1.4.43'}
            for i in case_data:
                case_schema = CaseDataSchema()
                data = case_schema.dump(i)
                text = data['text']
                case_text = eval(text)['root']
                # 筛选给定标识的测试用例
                new_data = Traverse().new_data(key_list, case_text)
                # 将筛选后的测试用例数据插入到版本测试用例中
                data_text['root']['children'].append(new_data)

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
                case_data.text = str(data_text)
                case_data.update_time = create_time
                case_data.update_user = create_user
                try:
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
            # 如果不存在，则插入数据
            else:
                data = CaseData(text=str(data_text), case_name_id=case_name_id, case_name=case_name,
                                create_time=create_time, create_user=create_user)
                db.session.add(data)
                db.session.commit()
            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'initJson': data_text
                }
                }
            return res
        else:
            res = {
                'code': code[3],
                'message': '请勿选择空测试用例',
                'data': {}
            }
            return res
