# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/1/11 15:34

"""
读取yaml文件的方法
"""

import os
import yaml
from Common.log import MyLog
from Common.public_method import PublicMethod


class YamlMethod:
    def __init__(self):
        self.log = MyLog

    def search_file(self, path, file_mame):
        """
        查找函数：path-待搜索目录路径 file_mame-待搜索文件名称
        """
        # 调用walk方法递归遍历path目录
        for root, dirs, files in os.walk(path):
            for name in files:
                if file_mame == name:
                    return os.path.join(root, name)

    def get_filepath(self, filename):
        # 获取项目路径
        current_path = os.getcwd()
        path_list = current_path.split('TPWeb-Python')
        path = path_list[0] + 'TPWeb-Python'
        # 获取指定文件路径
        file_path = self.search_file(path, filename)
        return file_path

    def read_data(self, filename):
        """
            读取YAML文件数据
            @:return filename 文件名称
        """

        file_path = self.get_filepath(filename)
        try:
            with open(file_path, 'rb') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except Exception as e:
            msg = '配置文件读取异常，请检查数据格式是否正确'
            self.log.error(msg + "ERROR:" + str(e))
            raise ValueError(msg)

    # 修改YAML文件数据--yaml配置文件需要是有两级数据
    def modify_data(self, filename, key_list, value):
        """
        修改配置文件
        :param filename: 文件名
        :param key_list: 修改的配置文件的层级目录，以list方式传入,[一级目录，二级目录，...]
        :param value: 新值
        :return:
        """
        # 定义白名单，白名单文件不允许修改
        white_list = ['']
        if filename in white_list:
            self.log.warning('系统信息配置文件不允许修改，请手动确认修改！')
            return False

        data = YamlMethod().read_data(filename)
        # 保留一份旧文件，用于报错时恢复
        old_data = data
        file_path = self.get_filepath(filename)

        try:
            with open(file_path, 'w', encoding="utf-8") as f:
                new_data = PublicMethod().modify_dict_value(data, key_list, value)
                yaml.dump(new_data, f)
                self.log.info('成功将 %s 的值修改为 %s' % (key_list[-1], value))
        except Exception as e:
            # 如果发生报错时，恢复初始文件
            with open(file_path, 'w', encoding="utf-8") as f:
                yaml.dump(old_data, f)
            msg = 'modify data error:{}'.format(e)
            self.log.error(msg)
            raise RuntimeError(msg)

        return YamlMethod().read_data(filename)


if __name__ == '__main__':
    print(YamlMethod().read_data('code.yaml')['code'][0])