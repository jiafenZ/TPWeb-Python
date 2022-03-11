# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/7 11:47

from Project.ApiTest.ApiProject.Database.baseUrl_database import UrlConfig, UrlConfigSchema
from Common.yaml_method import YamlMethod


class UrlList:
    """
    获取URL配置列表接口
    """

    @staticmethod
    def url_list(page, limit, config_name, project_name):
        """
        获取URL配置列表接口
        :param page: 页码
        :param limit: 每页多少条数据
        :param config_name: 配置名称
        :param project_name: 项目名称
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        if config_name == '' and project_name == '':
            data = UrlConfig.query.filter().paginate(page, limit)
        elif config_name != '' and project_name == '':
            data = UrlConfig.query.filter_by(configName=config_name).paginate(page, limit)
        elif config_name == '' and project_name != '':
            data = UrlConfig.query.filter_by(projectName=project_name).paginate(page, limit)
        else:
            data = UrlConfig.query.filter_by(configName=config_name, projectName=project_name).paginate(page, limit)
        info = []
        for i in data.items:
            mysql_schema = UrlConfigSchema()
            mysql_data = mysql_schema.dump(i)
            # 将单条URL信息添加到info中
            info.append(mysql_data)

        total = data.total
        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'mysqlList': info,
                'total': total
            }
        }

        return res
