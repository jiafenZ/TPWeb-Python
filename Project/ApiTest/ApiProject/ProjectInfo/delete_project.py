# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/25 18:51

from Common.mysql import db
from Project.ApiTest.ApiProject.Database.project_database import Project
from Common.yaml_method import YamlMethod
from sqlalchemy.exc import SQLAlchemyError


class DeleteProject:
    """
    删除项目接口
    """

    @staticmethod
    def delete_project(project_name):
        """
        删除项目信息
        :param project_name: 项目名称
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        project = Project.query.filter_by(projectName=project_name).first()

        if project is not None:
            try:
                db.session.delete(project)
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
                'message': '项目不存在'
            }
            return res
