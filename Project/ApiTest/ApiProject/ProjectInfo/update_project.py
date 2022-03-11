# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/25 18:26

import time
from Common.mysql import db
from Project.ApiTest.ApiProject.Database.project_database import Project
from sqlalchemy.exc import SQLAlchemyError
from Common.yaml_method import YamlMethod


class UpdateProject:
    """
    更新项目名称信息接口
    """

    @staticmethod
    def update_project(project_id, project_name, describe, update_user):
        """
        更新项目信息接口
        :param project_id: 项目ID
        :param project_name: 项目名称
        :param describe: 项目描述
        :param update_user: 更新人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        project = Project.query.filter_by(id=project_id).first()

        if project is not None:
            project.projectName = project_name
            project.describe = describe
            project.update_time = update_time
            project.update_user = update_user

            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                res = {
                    'code': code[6],
                    'data': [],
                    'message': '项目信息更新失败'
                }
                return res

            res = {
                'code': code[0],
                'data': [],
                'message': '项目信息更新成功'
            }
            return res

        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '项目不存在'
            }
            return res
