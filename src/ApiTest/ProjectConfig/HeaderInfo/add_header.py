# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/7 11:46
import time
from Common.mysql import db
from Common.yaml_method import YamlMethod
from src.ApiTest.ProjectConfig.Database.header_database import HeaderConfig


class AddHeaderInfo:
    """
    新增Header信息
    """
    @staticmethod
    def add_header_info(config_name, project_id, project_name, environment, header, create_user):
        """
        新增URL信息
        :param config_name: 配置名称
        :param project_id: 项目ID
        :param project_name: 项目名称
        :param environment: 运行环境
        :param header: header
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        info = HeaderConfig.query.filter_by(configName=config_name).first()
        if info is None:
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 项目信息插入数据库
            info = HeaderConfig(configName=config_name, projectId=project_id, projectName=project_name,
                             environment=environment, header=header, create_time=create_time, create_user=create_user)
            db.session.add(info)
            db.session.commit()

            res = {
                'code': code[0],
                'message': 'success',
                'data': {}
            }
            return res
        else:
            res = {
                'code': code[1],
                'message': '配置名称已存在',
                'data': {}
            }
            return res
