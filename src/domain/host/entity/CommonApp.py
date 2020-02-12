# coding=utf-8
import os
import stat
import logging
from domain.host.entity.App import App
from infrastucture.setting import *


class CommonApp(App):
    def __init__(self, app_name):
        super().__init__(app_name)

    def _get_install_path(self):
        return "%s/%s" % (install_dir, self.app_name)

    def start(self):
        os.chdir("%s/bin" % self._get_install_path())
        os.system("./startup.sh &")
        logging.info("%s 启动" % self.app_name)

    def stop(self):
        os.chdir("%s/bin" % self._get_install_path())
        os.system("./shutdown.sh")
        logging.info("%s 停止" % self.app_name)

    def install(self, install_file):
        if self.is_running:
            logging.info("%s 安装失败，当前程序正在运行" % self.app_name)
            return
        if install_file[0:2] == "./":
            install_file = install_file[2:]
        os.system("tar xvf %s -C %s" % (install_dir + os.sep + install_file, install_dir))
        os.chmod("%s/bin/startup.sh" % self._get_install_path(), stat.S_IRWXU)
        os.chmod("%s/bin/shutdown.sh" % self._get_install_path(), stat.S_IRWXU)
        logging.info("%s 已安装" % self.app_name)

    def uninstall(self):
        os.system("rm -rf %s" % self._get_install_path())
        logging.info("%s 已卸载" % self.app_name)
