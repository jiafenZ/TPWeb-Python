# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/1 15:21

import time
from Common.mysql import db
from Common.yaml_method import YamlMethod
from src.File.Database.file_data_database import FileData
from sqlalchemy.exc import SQLAlchemyError


class AddFileData:
    """
    新增/编辑文章
    """
    @staticmethod
    def add_file_data(content, file_name_id, file_name, is_open, is_edit, create_user):
        """
        新增测试用例
        :param content: 文章内容
        :param file_name_id: 文章名称ID
        :param file_name: 文章名称
        :param is_open: 隐私标志
        :param is_edit: 编辑权限标志
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 查询数据库中该文章是否存在
        file_data = FileData.query.filter_by(file_name_id=file_name_id).first()

        # 如果存在则进行数据迁移并更新数据
        if file_data:
            # 更新file_data数据
            file_data.content = content
            file_data.is_open = is_open
            file_data.is_edit = is_edit
            file_data.update_time = create_time
            file_data.update_user = create_user
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
        # 如果不存在，则插入数据
        else:
            data = FileData(content=content, file_name_id=file_name_id, file_name=file_name, is_open=is_open,
                            is_edit=is_edit, create_time=create_time, create_user=create_user)
            db.session.add(data)
            db.session.commit()

        res = {
            'code': code[0],
            'message': 'success',
            'data': {}
        }
        return res
