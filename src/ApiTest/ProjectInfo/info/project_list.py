# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/1/25 17:59

from src.ApiTest.ProjectInfo.Database.project_database import Project, ProjectSchema
from Common.yaml_method import YamlMethod


class ProjectList:
    """
    获取项目列表接口
    """

    @staticmethod
    def project_list():
        """
        获取项目列表接口
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        data = Project.query.all()
        info = []
        for i in data:
            project_schema = ProjectSchema()
            project_data = project_schema.dump(i)
            # 将单条数据库信息添加到info中
            info.append(project_data)

        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'projectList': info,
            }
        }

        return res
