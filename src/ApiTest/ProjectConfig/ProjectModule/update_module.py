# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/24 17:01

import time
from Common.mysql import db
from src.ApiTest.ProjectConfig.Database.module_database import Module, ModuleSchema
from sqlalchemy.exc import SQLAlchemyError
from Common.yaml_method import YamlMethod


class UpdateModule:
    """
    更新项目模块名称信息接口
    """

    @staticmethod
    def update_module(module_id, module_name, project_name, update_user):
        """
        更新项目模块信息接口
        :param module_id: 项目模块ID
        :param module_name: 项目模块名称
        :param project_name: 项目名称
        :param update_user: 更新人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        module = Module.query.filter_by(id=module_id).first()

        if module:
            module_info = Module.query.filter_by(moduleName=module_name).all()
            res_info = []
            for i in module_info:
                data_schema = ModuleSchema()
                name = data_schema.dump(i)
                res_info.append(name)
            if len(res_info) < 2:
                module.moduleName = module_name
                module.projectName = project_name
                module.update_time = update_time
                module.update_user = update_user

                try:
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    res = {
                        'code': code[6],
                        'data': [],
                        'message': '项目模块信息更新失败'
                    }
                    return res
                res = {
                    'code': code[0],
                    'data': [],
                    'message': '项目模块信息更新成功'
                }
                return res
            else:
                res = {
                    'code': code[1],
                    'data': [],
                    'message': '项目模块名已存在'
                }
                return res
        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '项目模块不存在'
            }
            return res
