# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/24 17:00

import time
from Common.mysql import db
from src.ApiTest.ProjectConfig.Database.module_database import Module
from Common.yaml_method import YamlMethod


class AddModule:
    """
    新增项目模块
    """
    @staticmethod
    def add_module(module_name, project_id, project_name, create_user):
        """
        新增项目
        :param module_name: 项目模块名称
        :param project_name: 项目名称
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        module = Module.query.filter_by(moduleName=module_name).first()
        if module is None:
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 项目信息插入数据库
            module = Module(moduleName=module_name, projectId=project_id, projectName=project_name, create_time=create_time, create_user=create_user)
            db.session.add(module)
            db.session.commit()

            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'moduleName': module_name
                }
            }
            return res
        else:
            res = {
                'code': code[1],
                'message': '项目模块名已存在',
                'data': {}
            }
            return res
