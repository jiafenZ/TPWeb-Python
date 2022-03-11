# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/25 16:30
import time
from Common.mysql import db
from Project.ApiTest.ApiProject.Database.project_database import Project
from Common.yaml_method import YamlMethod


class AddProject:
    """
    新增项目
    """
    @staticmethod
    def add_project(project_name, describe, create_user):
        """
        新增项目
        :param project_name: 项目名称
        :param describe: 项目描述
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        project = Project.query.filter_by(projectName=project_name).first()
        if project is None:
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 项目信息插入数据库
            project = Project(projectName=project_name, describe=describe, create_time=create_time,
                              create_user=create_user)
            db.session.add(project)
            db.session.commit()

            res = {
                'code': code[0],
                'message': 'success',
                'data': {
                    'projectName': project_name
                }
            }
            return res
        else:
            res = {
                'code': code[1],
                'message': '项目名已存在',
                'data': {}
            }
            return res
