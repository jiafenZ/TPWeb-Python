# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/7 11:46

import time
from Common.mysql import db
from src.ApiTest.ProjectConfig.Database.baseUrl_database import UrlConfig
from sqlalchemy.exc import SQLAlchemyError
from Common.yaml_method import YamlMethod


class UpdateUrlInfo:
    """
    更新URL信息接口
    """

    @staticmethod
    def update_url_info(config_id, config_name, project_id, project_name, environment, url, update_user):
        """
        更新URL配置信息
        :param config_id: 配置ID
        :param config_name: 配置名称
        :param project_id: 项目ID
        :param project_name: 项目名称
        :param environment: 运行环境
        :param url: base url
        :param update_user: 更新人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        info = UrlConfig.query.filter_by(id=config_id).first()

        if info:
            url_info = UrlConfig.query.filter_by(configName=config_name).first()
            if url_info is None:
                info.configName = config_name
                info.projectId = project_id
                info.projectName = project_name
                info.environment = environment
                info.base_url = url
                info.update_time = update_time
                info.update_user = update_user

                try:
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    res = {
                        'code': code[6],
                        'data': [],
                        'message': 'URL信息更新失败'
                    }
                    return res

                res = {
                    'code': code[0],
                    'data': [],
                    'message': 'URL信息更新成功'
                }
                return res
            else:
                res = {
                    'code': code[1],
                    'data': [],
                    'message': 'URL名已存在'
                }
                return res
        else:
            res = {
                'code': code[3],
                'data': [],
                'message': 'URL信息不存在'
            }
            return res
