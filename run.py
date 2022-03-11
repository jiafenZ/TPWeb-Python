# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2021/12/31 16:18

from Project.User.Api.user_api import app
from Project.ApiTest.ApiProject.Api.header_api import app
from Project.ApiTest.ApiProject.Api.project_api import app
from Project.ApiTest.ApiProject.Api.url_api import app
from Project.ApiTest.ApiProject.Api.mysql_api import app
from Project.Case.Api.case_name_api import app
from Project.Case.Api.case_data_api import app
from Project.File.Api.file_name_api import app
from Project.File.Api.file_data_api import app
from Project.TodoList.Api.todo_list_api import app

app.run(host='192.168.0.114', port=8888, debug=True)
