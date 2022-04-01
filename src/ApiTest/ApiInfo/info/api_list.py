# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/28 11:59

from src.ApiTest.ApiInfo.Database.api_database import ApiInfo, ApiInfoSchema
from Common.yaml_method import YamlMethod


class ApiList:
    """
    获取接口列表接口
    """

    @staticmethod
    def api_list(page, limit, api_name, module_name, project_name):
        """
        获取接口列表接口
        :param page: 页码
        :param limit: 每页多少条数据
        :param api_name: 接口名称
        :param module_name: 模块名称
        :param project_name: 项目名称
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        if api_name == '' and module_name == '' and project_name == '':
            data = ApiInfo.query.filter().paginate(page, limit)
        elif api_name != '' and module_name == '' and project_name == '':
            data = ApiInfo.query.filter_by(apiName=api_name).paginate(page, limit)
        elif api_name != '' and module_name != '' and project_name == '':
            data = ApiInfo.query.filter_by(apiName=api_name, moduleName=module_name).paginate(page, limit)
        elif api_name != '' and module_name == '' and project_name != '':
            data = ApiInfo.query.filter_by(apiName=api_name, projectName=project_name).paginate(page, limit)
        elif api_name == '' and module_name != '' and project_name != '':
            data = ApiInfo.query.filter_by(moduleName=module_name, projectName=project_name).paginate(page, limit)
        elif api_name == '' and module_name == '' and project_name != '':
            data = ApiInfo.query.filter_by(projectName=project_name).paginate(page, limit)
        elif api_name == '' and module_name != '' and project_name == '':
            data = ApiInfo.query.filter_by(moduleName=module_name).paginate(page, limit)
        else:
            data = ApiInfo.query.filter_by(apiName=api_name, moduleName=module_name, projectName=project_name).paginate(page, limit)
        info = []
        for i in data.items:
            api_schema = ApiInfoSchema()
            api_data = api_schema.dump(i)
            # 将单条数据库信息添加到info中
            info.append(api_data)

        total = data.total
        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'apiList': info,
                'total': total
            }
        }

        return res
