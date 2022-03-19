# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2021/12/31 16:18

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

app.run(host='192.168.1.102', port=8888, debug=True)
