# -*- coding: utf-8 -*-
# @Author:Jerry

import os,sys;sys.path.append(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], "..")))
from Common.log import MyLog


def update_pip():
    pip_query_cmd = 'pip list --outdated --format=freeze'
    MyLog.info('检查可升级pip包:')
    with os.popen(pip_query_cmd) as pip_query:
        data = pip_query.read()
        MyLog.info(data)
    package_list = data.split('\n')

    for package in package_list:
        pip_package = str(package).split('==')[0]
        update_cmd = 'pip install --upgrade '+pip_package

        MyLog.info('更新pip包中：{}'.format(update_cmd))
        status = os.system(update_cmd)
        if int(status) == 0:
            MyLog.info('-----------------包（{}）更新成功 ^_^\n'.format(pip_package))
        else:
            MyLog.error('-----------------包（{}）更新失败!!!命令--{}\n'.format(pip_package, update_cmd))
    MyLog.info('pip包更新完成-------------------------------------')


if __name__ == '__main__':
    update_pip()
