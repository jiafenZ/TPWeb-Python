# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/28 11:19

import time
from Common.mysql import db
from src.ApiTest.ApiInfo.Database.api_database import ApiInfo
from Common.yaml_method import YamlMethod


class AddApi:
    """
    新增基础接口
    """
    @staticmethod
    def add_api(api_name, project_name, module_name, path, method, pre_parameter, headers, debug_headers, body,
                debug_body, after_parameter, assert_sql, assert_parameter, create_user):
        """
        新增基础接口
        :param api_name: 接口名称
        :param project_name: 项目名称
        :param module_name: 模块名称
        :param path: 请求路径
        :param method: 请求方法
        :param pre_parameter: 前置参数
        :param headers: 请求头
        :param debug_headers: 调试请求头
        :param body: 请求体
        :param debug_body: 调试请求体
        :param after_parameter: 响应参数提取
        :param assert_sql: SQL断言
        :param assert_parameter: 断言参数
        :param create_user: 创建人
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 项目信息插入数据库
        info = ApiInfo(apiName=api_name, projectName=project_name, moduleName=module_name, path=path, method=method,
                       pre_parameter=pre_parameter, headers=headers, debug_headers=debug_headers, body=body,
                       debug_body=debug_body, after_parameter=after_parameter, assert_sql=assert_sql,
                       assert_parameter=assert_parameter, create_time=create_time, create_user=create_user)
        db.session.add(info)
        db.session.commit()

        res = {
            'code': code[0],
            'message': 'success',
            'data': {}
        }
        return res
