# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/1 15:52

from Common.yaml_method import YamlMethod
from src.File.Database.file_data_database import FileData, FileDataSchema
from src.File.Database.file_name_database import FileName, FileNameSchema


class GetFileData:
    """
    获取文章内容接口
    """

    @staticmethod
    def get_file_data(file_name_id, request_user):
        """
        获取文章内容接口
        :param file_name_id: 文章名称ID
        :param request_user: 请求人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']
        # 定义是否存在下级目录标志变量
        is_name = '0'

        # 查询数据库中的文章内容
        file_data = FileData.query.filter_by(file_name_id=file_name_id).first()
        file_schema = FileDataSchema()
        data = file_schema.dump(file_data)

        if data:
            file_content = data['content']
            create_user = data['create_user']
            is_open = data['is_open']
            edit = data['is_edit']
        else:
            # 查询该文章名称有没有下级目录
            name_data = FileName.query.all()
            for i in name_data:
                file_name_schema = FileNameSchema()
                file_name_data = file_name_schema.dump(i)
                if file_name_data['parent_id'] == file_name_id:
                    is_name = '1'

            file_content = ''
            is_open = ''
            edit = ''
            create_user = ''

        if is_open == '1':
            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'initJson': file_content,
                    'read': is_open,
                    'edit': edit,
                    'file_name_id': file_name_id,
                    'is_name': is_name
                }
            }
        else:
            if create_user == request_user:
                res = {
                    'code': code[0],
                    'message': 'success',
                    'data': {
                        'initJson': file_content,
                        'read': is_open,
                        'edit': '1',
                        'file_name_id': file_name_id,
                        'is_name': is_name
                    }
                }
            else:
                res = {
                    'code': code[0],
                    'message': 'success',
                    'data': {
                        'initJson': '',
                        'read': is_open,
                        'edit': edit,
                        'file_name_id': file_name_id,
                        'is_name': is_name
                    }
                }

        return res
