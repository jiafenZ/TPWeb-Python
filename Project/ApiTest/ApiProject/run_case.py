# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/3/11 10:33

# 测试数据格式示例---还需要考虑环境信息、项目信息、是否需要断言、是否需要加解密等

data = [
    {'data': {'url': '', 'path': '', 'body': ''}},
    {'data': {'url': '', 'path': '', 'body': ''}},
    {'data': [{'data': {'url': '', 'path': '', 'body': ''}}, {'data': {'url': '', 'path': '', 'body': ''}}]},
    {'data': [{'data': {'url': '', 'path': '', 'body': ''}},
              {'data': [{'data': {'url': '', 'path': '', 'body': ''}}, {'data': {'url': '', 'path': '', 'body': ''}}]}
              ]},
    {'data': {'url': '', 'path': '', 'body': ''}}
]
