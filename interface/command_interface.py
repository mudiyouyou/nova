# coding=utf-8
"""
支持如下命令:
nova stop 程序安装目录
nova start 程序安装目录
nova install 程序安装目录 安装包
nova uninstall 程序安装目录
nova backup 程序安装目录
nova rollback 程序安装目录
nova log 程序安装目录
nova list_app 显示所有运行时Java程序
"""
import sys
import logging
from application.service import app_service


def command():
    if len(sys.argv) >= 2:
        action = sys.argv[1]
        params = sys.argv[2:]
        try:
            sys.modules[__name__].__getattribute__(action)(params)
            return
        except Exception as e:
            print(e)
            logging.info(sys.modules[__name__].__doc__)
            return
    logging.info(sys.modules[__name__].__doc__)


def start(params):
    """
    运行程序
    运行程序安装目录下bin目录下的startup.sh脚本
    命令格式:start 程序安装目录名称
    """
    if len(params) == 1:
        app_service.start(params[0])
    else:
        logging.info(__doc__)


def stop(params):
    """
    停止程序
    运行程序安装目录下bin目录下的shutdown.sh脚本
    命令格式:stop 程序安装目录名称
    """
    if len(params) == 1:
        app_service.stop(params[0])
    else:
        logging.info(__doc__)


def install(params):
    """
    安装程序
    自动解压缩安装包,修改bin目录下*.sh的权限
    命令格式:install 程序安装目录名称 安装程序包(.war  .tar.gz)
    """
    if len(params) == 2:
        app_service.install(params[0], params[1])
    else:
        logging.info(install.__doc__)


def backup(params):
    """
    备份程序
    拷贝程序到备份目录下,备份目录为backup_dir/当前日期,backup_dir为~/.nova 文件中指定
    命令格式:backup 程序安装目录名称
    """
    if len(params) == 1:
        app_service.backup(params[0])
    else:
        logging.info(backup.__doc__)


def rollback(params):
    """
    回滚程序
    拷贝backup_dir/当前日期/程序名称目录到安装目录,backup_dir为~/.nova 文件中指定
    命令格式:rollback 程序安装目录名称
    """
    if len(params) == 1:
        app_service.rollback(params[0])
    else:
        logging.info(rollback.__doc__)


def uninstall(params):
    """
    卸载程序
    命令格式:uninstall 程序安装目录名称
    """
    if len(params) == 1:
        app_service.uninstall(params[0])
    else:
        logging.info(uninstall.__doc__)


def log(params):
    """
    命令格式:log 程序安装目录名称
    """
    if len(params) == 1:
        app_service.get_tail_of_log(params[0]).start()
        return
    else:
        logging.info(log.__doc__)


def list_app(params):
    """
    列表已安装的所有程序
    显示安装目录下所有程序，格式如下
    名称:{程序名称} 运行状态:{True|False} CPU:{百分比} 内存:{单位MB}
    命令格式:list_app
    """
    try:
        app_service.list_app()
    except RuntimeError:
        logging.info(list_app.__doc__)
