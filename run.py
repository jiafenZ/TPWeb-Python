# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2021/12/31 16:18
from gevent import pywsgi
from Common.yaml_method import YamlMethod
from src.User.Api.user_api import app
from src.ApiTest.ProjectConfig.Api.header_api import app
from src.ApiTest.ProjectInfo.Api.project_api import app
from src.ApiTest.ProjectConfig.Api.url_api import app
from src.ApiTest.ProjectConfig.Api.mysql_api import app
from src.Case.Api.case_name_api import app
from src.Case.Api.case_data_api import app
from src.File.Api.file_name_api import app
from src.File.Api.file_data_api import app
from src.TodoList.Api.todo_list_api import app
from src.ApiTest.TestData.Api.data_api import app
from src.ApiTest.ProjectConfig.Api.module_api import app
from src.ApiTest.ApiInfo.Api.api_info_api import app

evn = YamlMethod().read_data('environment.yaml')['evn']
server = YamlMethod().read_data('account_info.yaml')['server'][evn]
host = server[0]
port = server[1]

if evn == 'dev':
    app.run(host=host, port=port, debug=True)
else:
    server = pywsgi.WSGIServer((host, port), app)
    server.serve_forever()
