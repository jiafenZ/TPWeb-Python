# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/3/1 18:37

import time
from Common.mysql import db
from sqlalchemy.exc import SQLAlchemyError
from Common.yaml_method import YamlMethod
from Project.File.Database.file_name_database import FileName
from Project.File.Database.file_data_database import FileData


class UpdateFileName:
    """
    修改文章名称信息接口
    """

    @staticmethod
    def update_file_name(file_name_id, file_name, update_user):
        """
        修改文章名称信息接口
        :param file_name_id: 文章名称ID
        :param file_name: 文章名称
        :param update_user: 更新人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        fileName = FileName.query.filter_by(id=file_name_id).first()

        if fileName:
            fileName.file_name = file_name
            fileName.update_time = update_time
            fileName.update_user = update_user
            file_data = FileData.query.filter_by(file_name_id=file_name_id).first()
            if file_data:
                file_data.file_name = file_name
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                res = {
                    'code': code[6],
                    'data': [],
                    'message': '文章名称更新失败'
                }
                return res

            res = {
                'code': code[0],
                'data': [],
                'message': '文章名称更新成功'
            }
            return res

        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '文章名称不存在'
            }
            return res
