# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2021/12/31 16:18

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

server = YamlMethod().read_data('account_info.yaml')['server']
host = server[0]
port = server[1]

app.run(host=host, port=port, debug=True)
