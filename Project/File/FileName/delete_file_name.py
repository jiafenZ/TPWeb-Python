# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/3/1 18:36

import time
from Common.mysql import db
from Common.yaml_method import YamlMethod
from sqlalchemy.exc import SQLAlchemyError
from Project.File.Database.file_name_database import FileName, FileNameSchema
from Project.File.Database.file_data_database import FileData, FileDataSchema
from Project.File.Database.file_data_history_database import FileDataHistory, FileDataHistorySchema


class DeleteFileName:
    """
    删除测试文章名称
    """

    @staticmethod
    def delete_file_name(file_name_id, create_user):
        """
        删除测试用例名称
        :param file_name_id: 文章名称ID
        :param create_user: 删除人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        # 查询文章名称是否存在
        file_name_data = FileName.query.filter_by(id=file_name_id).first()
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if file_name_data:
            # 查询该名称是否存在文章
            file_data = FileData.query.filter_by(file_name_id=file_name_id).first()
            if file_data:
                data_schema = FileDataSchema()
                old_data = data_schema.dump(file_data)
                # 将表中的旧数据迁移到file_data_history表中
                file_id = old_data['id']
                content = old_data['content']
                file_name_id = old_data['file_name_id']
                file_name = old_data['file_name']
                is_open = old_data['is_open']
                is_edit = old_data['is_edit']
                data = FileDataHistory(file_id=file_id, content=content, file_name_id=file_name_id, file_name=file_name,
                                       is_open=is_open, is_edit=is_edit, create_time=create_time,
                                       create_user=create_user)
                db.session.add(data)
                db.session.commit()
                # 删除文章
                try:
                    db.session.delete(file_data)
                    db.session.commit()
                except SQLAlchemyError as e:
                    db.session.rollback()
                    res = {
                        'code': code[5],
                        'data': [],
                        'message': '删除文章失败'
                    }
                    return res
            # 删除文章名称
            try:
                db.session.delete(file_name_data)
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
                'message': '文章名称不存在'
            }
            return res
