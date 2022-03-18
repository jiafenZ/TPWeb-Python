# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/1 18:37

from Common.yaml_method import YamlMethod
from src.File.Database.file_name_database import FileName, FileNameSchema


class FileNameTree:
    """
    获取文章名称,并转换成树形结构
    """

    @staticmethod
    def file_name_tree():
        """
        获取文章名称,并转换成树形结构
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        data = FileName.query.all()
        info = []
        max_id = 0
        for i in data:
            file_name_schema = FileNameSchema()
            file_name_data = file_name_schema.dump(i)
            # 移除时间信息
            file_name_data.pop('update_user')
            file_name_data.pop('update_time')
            file_name_data.pop('create_time')
            file_name_data.pop('create_user')
            # 判断是否是最大id
            if file_name_data['id'] > max_id:
                max_id = file_name_data['id']
            # 将单条数据库信息添加到info中
            info.append(file_name_data)

        new = '[]'
        while len(info) > 0:
            for info_key in info:
                if info_key['parent_id'] == 0:
                    str_info_key = '"parent_id": %s,' % info_key['parent_id'] + '"file_name": "%s",' \
                                   % info_key['file_name'] + '"id": %s,' % info_key['id'] + '"children": [],'
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
                            insert_str = '"parent_id": %s,' % info_key['parent_id'] + '"file_name": "%s",' \
                                         % info_key['file_name'] + '"id": %s,' % info_key['id'] + '"children": [],'
                            new = new[0:end] + '{' + insert_str + '}' + ',' + new[end:]
                            info.remove(info_key)
                        else:
                            pass

        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'FileNameTree': eval(new),
                'startId': max_id
            }
        }

        return res
