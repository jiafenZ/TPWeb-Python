# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/2/7 11:47

from Common.mysql import db
from src.ApiTest.ProjectConfig.Database.baseUrl_database import UrlConfig
from Common.yaml_method import YamlMethod
from sqlalchemy.exc import SQLAlchemyError


class DeleteUrlInfo:
    """
    删除URL配置信息接口
    """

    @staticmethod
    def delete_url_info(config_name):
        """
        删除URL配置信息
        :param config_name: 配置名称
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        info = UrlConfig.query.filter_by(configName=config_name).first()

        if info is not None:
            try:
                db.session.delete(info)
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
                'message': 'URL配置信息不存在'
            }
            return res
