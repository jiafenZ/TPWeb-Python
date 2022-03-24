# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/24 17:00

from Common.mysql import db
from src.ApiTest.ProjectConfig.Database.module_database import Module
from Common.yaml_method import YamlMethod
from sqlalchemy.exc import SQLAlchemyError


class DeleteModule:
    """
    删除项目模块接口
    """

    @staticmethod
    def delete_module(module_name):
        """
        删除项目模块信息
        :param module_name: 项目模块名称
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        module = Module.query.filter_by(moduleName=module_name).first()

        if module is not None:
            try:
                db.session.delete(module)
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
                'message': '项目模块不存在'
            }
            return res
