# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/1 18:36

import time
from Common.mysql import db
from Common.yaml_method import YamlMethod
from src.File.Database.file_name_database import FileName


class AddFileName:
    """
    新增文章名称
    """
    @staticmethod
    def add_file_name(file_name, parent_id, create_user):
        """
        新增文章名称
        :param file_name: 文章名称
        :param parent_id: 文章名称父ID
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        data = FileName(file_name=file_name, parent_id=parent_id, create_time=create_time, create_user=create_user)
        db.session.add(data)
        db.session.commit()

        res = {
            'code': code[0],
            'message': 'success',
            'data': {}
        }
        return res
