# -*- coding: utf-8 -*-
# @Author:Jerry


import os,sys;sys.path.append(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], "..")))
from Common.log import MyLog


def install_pip():
    """
    # 该方法用于自动安装pip包，跑完该方法大部分包能够安装完成，其他的在编写脚本中报错再手动安装下就行
    :return:
    """

    MyLog.info('即将自动安装pip列表')
    pip_u = 'pip install -U pip'
    # 更新pip工具
    MyLog.info('更新pip中...')
    status = os.system(pip_u)
    if int(status) == 0:
        MyLog.info('pip升级成功 ^_^')
    else:
        MyLog.error('pip升级失败！！！')

    # 验证是否已安装包，已安装时跳过
    f = open("requirements.txt")  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        pip_package = str(line).split('==')[0]
        install_cmd = 'pip install ' + pip_package
        show_pip_cmd = 'pip show '+pip_package
        f_show = os.popen(show_pip_cmd, "r")
        try:
            pip_log = f_show.read()
        except Exception:
            pip_log = 'null'
        if pip_log[:4] != 'Name':
            MyLog.info('安装pip包中：{}'.format(install_cmd))
            status = os.system(install_cmd)
            if int(status) == 0:
                MyLog.info('包（{}）安装成功 ^_^'.format(pip_package))
            else:
                MyLog.error('包（{}）安装失败!!!'.format(pip_package))
        else:
            MyLog.info('包（{}）已安装，跳过'.format(pip_package))
        f_show.close()
        line = f.readline()
    f.close()

    MyLog.info('pip列表已经安装完成---------')
    return True


if __name__ == '__main__':
    install_pip()
