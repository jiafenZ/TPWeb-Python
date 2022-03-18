# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2021/12/31 16:18

from src.TodoList.Api.todo_list_api import app

app.run(host='192.168.1.102', port=8888, debug=True)
