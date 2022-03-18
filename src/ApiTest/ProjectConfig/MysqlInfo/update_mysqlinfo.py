# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/7 11:46

import time
from Common.mysql import db
from src.ApiTest.ProjectConfig.Database.mysqlConfig_database import MysqlConfig
from sqlalchemy.exc import SQLAlchemyError
from Common.yaml_method import YamlMethod


class UpdateMysqlInfo:
    """
    更新数据库信息接口
    """

    @staticmethod
    def update_mysql_info(config_id, config_name, project_id, project_name, environment, host, port, user, password, update_user):
        """
        更新数据库配置信息
        :param config_id: 配置ID
        :param config_name: 配置名称
        :param project_id: 项目ID
        :param project_name: 项目名称
        :param environment: 运行环境
        :param host: host
        :param port: 端口号
        :param user: 用户名
        :param password: 密码
        :param update_user: 更新人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        info = MysqlConfig.query.filter_by(id=config_id).first()

        if info:
            mysql_info = MysqlConfig.query.filter_by(configName=config_name).first()
            if mysql_info is None:
                info.configName = config_name
                info.projectId = project_id
                info.projectName = project_name
                info.environment = environment
                info.host = host
                info.port = port
                info.user = user
                info.password = password
                info.update_time = update_time
                info.update_user = update_user

                try:
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    res = {
                        'code': code[6],
                        'data': [],
                        'message': '数据库信息更新失败'
                    }
                    return res

                res = {
                    'code': code[0],
                    'data': [],
                    'message': '数据库信息更新成功'
                }
                return res
            else:
                res = {
                    'code': code[1],
                    'data': [],
                    'message': '数据库名已存在'
                }
                return res
        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '数据库信息不存在'
            }
            return res
