# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/1/11 15:36

"""
封装打印和保存日志的方法

"""

import logging
import os
import time
import stat
import datetime

LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

logger = logging.getLogger()
level = 'default'


def create_file(filename):
    """
    生成日志文件方法，如果不存在文件，则生成文件，如果存在，则打开日志文件进行写入操作
    :param filename:
    :return:
    """
    path = filename[0:filename.rfind('/')]
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(filename):
        fd = open(filename, mode='w', encoding='utf-8')
        fd.close()
    else:
        pass
    # 赋予文件777的权限,防止不同用户访问时报错
    try:
        os.chmod(filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except Exception as e:
        print('设置日志文件权限错误，error：{}'.format(e))


def delete_file():
    """
    删除5天前的过期日志文件
    :return:
    """

    filename_list = []
    for i in range(5):
        filename_time = str(datetime.datetime.today().date() + datetime.timedelta(days=-i))

        log_filename = 'log_' + filename_time + '.log'
        err_filename = 'err_' + filename_time + '.log'
        filename_list.append(log_filename)
        filename_list.append(err_filename)
    # 读取日志文件Log目录下的日志文件名
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\Log\\'
    for path, subdirs, files in os.walk(path):
        for file in filename_list:
            if file in files:
                files.remove(file)
        # 如果文件存在，则删除文件
        for del_file in files:
            filename_path = path + str(del_file)
            os.remove(filename_path)


def set_handler(levels):
    if levels == 'error':
        logger.addHandler(MyLog.err_handler)
    logger.addHandler(MyLog.handler)


def remove_handler(levels):
    if levels == 'error':
        logger.removeHandler(MyLog.err_handler)
    logger.removeHandler(MyLog.handler)


def get_current_time():
    return datetime.datetime.now().strftime(MyLog.date)


class MyLog:
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    log_file = path + '/Log/log_' + local_time + '.log'
    err_file = path + '/Log/err_' + local_time + '.log'
    logger.setLevel(LEVELS.get(level, logging.NOTSET))
    delete_file()
    create_file(log_file)
    create_file(err_file)
    date = '%Y-%m-%d %H:%M:%S.%f'

    handler = logging.FileHandler(log_file, encoding='utf-8')
    err_handler = logging.FileHandler(err_file, encoding='utf-8')

    @staticmethod
    def debug(log_meg):
        set_handler('debug')
        logger.debug("[DEBUG " + get_current_time() + "]" + str(log_meg))
        print("[DEBUG]" + str(log_meg))
        remove_handler('debug')

    @staticmethod
    def info(log_meg):
        set_handler('info')
        logger.info("[INFO " + get_current_time() + "]" + str(log_meg))
        print("[INFO]" + str(log_meg))
        remove_handler('info')

    @staticmethod
    def warning(log_meg):
        set_handler('warning')
        logger.warning("[WARNING " + get_current_time() + "]" + str(log_meg))
        print("\033[1;33;0m[WARNING]" + str(log_meg) + '\033[0m')
        remove_handler('warning')

    @staticmethod
    def error(log_meg):
        try:
            raise Exception
        except:
            import sys
            f = sys.exc_info()[2].tb_frame.f_back
        datas = 'The error source: ' + f.f_code.co_filename + ' ' + f.f_code.co_name + ' ' + str(f.f_lineno)
        set_handler('error')
        logger.error("[ERROR " + get_current_time() + "]" + str(log_meg))
        logger.error(datas)
        print("\033[1;31;0m[ERROR]" + str(log_meg) + '\033[0m')
        remove_handler('error')

    @staticmethod
    def critical(log_meg):
        set_handler('critical')
        logger.error("[CRITICAL " + get_current_time() + "]" + str(log_meg))
        print("[CRITICAL]" + str(log_meg))
        remove_handler('critical')


if __name__ == "__main__":
    MyLog.info("This is info message")
    delete_file()
