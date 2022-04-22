# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/28 11:45

import time
from Common.mysql import db
from src.ApiTest.ApiInfo.Database.api_database import ApiInfo
from sqlalchemy.exc import SQLAlchemyError
from Common.yaml_method import YamlMethod


class UpdateApiInfo:
    """
    更新接口信息接口
    """

    @staticmethod
    def update_api_info(api_id, api_name, project_name, module_name, path, method, pre_parameter, headers, debug_headers, body,
                        debug_body, after_parameter, assert_sql, assert_parameter, update_user):
        """
        更新接口信息接口
        :param api_id: 接口ID
        :param api_name: 接口名称
        :param project_name: 项目名称
        :param module_name: 模块名称
        :param path: 请求路径
        :param method: 请求路径
        :param pre_parameter: 前置参数
        :param headers: 请求头
        :param debug_headers: 调试请求头
        :param body: 请求体
        :param debug_body: 调试请求体
        :param after_parameter: 响应参数提取
        :param assert_sql: SQL断言
        :param assert_parameter: 断言参数
        :param update_user: 更新人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        info = ApiInfo.query.filter_by(id=api_id).first()

        if info:
            info.apiName = api_name
            info.projectName = project_name
            info.moduleName = module_name
            info.path = path
            info.method = method
            info.pre_parameter = pre_parameter
            info.headers = headers
            info.debug_headers = debug_headers
            info.body = body
            info.debug_body = debug_body
            info.after_parameter = after_parameter
            info.assert_sql = assert_sql
            info.assert_parameter = assert_parameter
            info.update_user = update_user
            info.update_time = update_time
            try:
                db.session.commit()
            except SQLAlchemyError:
                db.session.rollback()
                res = {
                    'code': code[6],
                    'data': [],
                    'message': '接口信息更新失败'
                }
                return res
            res = {
                'code': code[0],
                'data': [],
                'message': '接口信息更新成功'
            }
            return res
        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '接口信息不存在'
            }
            return res
