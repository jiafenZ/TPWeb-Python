# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/24 17:01

from src.ApiTest.ProjectConfig.Database.module_database import Module, ModuleSchema
from Common.yaml_method import YamlMethod


class ModuleList:
    """
    获取项目模块列表接口
    """

    @staticmethod
    def module_list(page, limit, module_name, project_name):
        """
        获取URL配置列表接口
        :param page: 页码
        :param limit: 每页多少条数据
        :param module_name: 模块名称
        :param project_name: 项目名称
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        if module_name == '' and project_name == '':
            data = Module.query.filter().paginate(page, limit)
        elif module_name != '' and project_name == '':
            data = Module.query.filter_by(moduleName=module_name).paginate(page, limit)
        elif module_name == '' and project_name != '':
            data = Module.query.filter_by(projectName=project_name).paginate(page, limit)
        else:
            data = Module.query.filter_by(moduleName=module_name, projectName=project_name).paginate(page, limit)
        info = []
        for i in data.items:
            mysql_schema = ModuleSchema()
            mysql_data = mysql_schema.dump(i)
            # 将单条header信息添加到info中
            info.append(mysql_data)

        total = data.total
        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'moduleList': info,
                'total': total
            }
        }

        return res
