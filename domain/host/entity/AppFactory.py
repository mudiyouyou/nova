# coding=utf-8
import os

from domain.host.entity.CommonApp import CommonApp
from domain.host.entity.TomcatApp import TomcatApp
from infrastucture.setting import *


def create(app_name, install_file=None):
    if install_file:
        if install_file.endswith(".tar") or install_file.endswith(".gz"):
            return CommonApp(app_name)
        if install_file.endswith(".war"):
            return TomcatApp(app_name)
        else:
            raise TypeError("不支持该文件安装")
    else:
        if app_name[-1] == "/":
            app_name = app_name[0:-1]
        subs = os.listdir(install_dir + os.sep + app_name)
        if tomcat_dir in subs:
            return TomcatApp(app_name)
        else:
            return CommonApp(app_name)
