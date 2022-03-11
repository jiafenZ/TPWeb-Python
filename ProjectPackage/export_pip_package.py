# -*- coding: utf-8 -*-
# @Author:Jerry

import os,sys;sys.path.append(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], "..")))
from Common.log import MyLog

MyLog.info('即将导出pip安装包')

pip_cmd = 'pip freeze >requirements.txt'


MyLog.info('导出pip包中')
os.system(pip_cmd)
