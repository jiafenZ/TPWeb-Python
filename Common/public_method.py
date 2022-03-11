# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/11 15:37

"""
封装公共基础方法
"""

import os
import time
import hashlib
from Common.log import MyLog
from functools import wraps


class PublicMethod:
    def __init__(self):
        self.log = MyLog

    def get_dict_key(self, you_dict):
        """
        该方法用于获取字典类型的所有key，包含子类中的key
        :param you_dict:

        :return tmp: 返回排序后的keylist
        """
        tmp = []
        self.log.info('你需要获取所有key的字典为：{}'.format(you_dict))
        if isinstance(you_dict, dict):
            for k, v in you_dict.items():
                tmp.append(k)
                # 判断数据类型是否字典，列表
                if isinstance(v, (dict, list)):
                    # 重复调用自己
                    ret = self.get_dict_key(v)
                    tmp += ret
        if isinstance(you_dict, list):
            for x in you_dict:
                if isinstance(x, (dict, list)):
                    ret = self.get_dict_key(x)
                    tmp += ret
        # 对list进行排序
        tmp.sort()
        self.log.info('你需要获取所有key_list为：{}'.format(tmp))
        return tmp

    def modify_dict_value(self, you_dict, key_list, value):
        """
        用于修改字典中的value值，实现不确定长度字典的修改
        :param you_dict: 要修改的字典
        :param key_list:
        :param value:
        :return:
        """
        if type(you_dict) is not dict:
            msg = '所需要的参数应该是dict格式，请确认你的传参；you_dict：{}'.format(you_dict)
            self.log.error(msg)
            raise TypeError(msg)
        if type(key_list) is not list:
            msg = '所需要的参数应该是list格式，请确认你的传参；key_list：{}'.format(you_dict)
            self.log.error(msg)
            raise TypeError(msg)
        yaml_data = you_dict

        # 首先将字典逐级读取出来，写入到data_list中
        tem = None
        data_list = []
        for n in range(len(key_list)):
            try:
                if n == 0:
                    tem = yaml_data[key_list[n]]
                else:
                    tem = tem[key_list[n]]
            except Exception as e:
                msg = '源数据没有key-{}！error:{}'.format(key_list[n], e)
                self.log.error(msg)
                raise TypeError(msg)
            data_list.insert(0, tem)

        # 修改需要修改的值后再封装字典
        new_dict = {}
        for m in range(len(key_list)):
            tem_dict = {}
            tem_list = []
            if m == 0:
                # 修改为需要修改的值
                tem_dict[key_list[-m - 1]] = value
            else:
                # 不修改的直接封装起来
                if isinstance(key_list[-m - 1], str):
                    tem_dict[key_list[-m - 1]] = new_dict
                elif isinstance(key_list[-m - 1], list):
                    tem_list = data_list[m + 1]
                    tem_list[key_list[-m - 1]] = new_dict
                else:
                    msg = '暂时不支持该数据格式！{}'.format(key_list[-m - 1])
                    self.log.error(msg)
                    raise TypeError(msg)
            new_dict = tem_dict

            if m == len(key_list) - 1:
                # 更新最外层的key
                yaml_data.update(new_dict)
                break
            else:
                # 逐层封装更新字典
                p = data_list[m + 1]
                if isinstance(p, dict):
                    p.update(new_dict)
                elif isinstance(p, list):
                    p = tem_list
                else:
                    msg = '暂时不支持该数据格式！{}'.format(p)
                    self.log.error(msg)
                    raise TypeError(msg)
                new_dict = p
        return yaml_data

    def empty(self, file):
        """
        删除指定路径的文件
        file: 文件路径
        """
        if os.path.exists(file):
            os.remove(file)
        else:
            pass


def md_5(password):
    """
    密码md5加密方法
    :param password: 登录密码
    :return: 返回加密后的密码
    """
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))

    return md5.hexdigest()


def time_decorator(func):
    """
    统计方法运行时间修饰器
    :param func:
    :return:
    """

    @wraps(func)
    def run_time(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        running_time = end - start
        return func(*args, **kwargs), {'程序运行时间': '%.2f' % running_time + ' 秒'}
    return run_time
