# coding=utf-8
import shutil
import logging
from domain.host.entity.App import App
from infrastucture.setting import *


class TomcatApp(App):
    def __init__(self, app_name):
        super().__init__(app_name)
        self.tomcat_path = "%s/%s/%s" % (install_dir, self.app_name, tomcat_dir)

    def _get_install_path(self):
        return "%s/webapps" % self.tomcat_path

    def start(self):
        os.chdir("%s/bin" % self.tomcat_path)
        os.system("./startup.sh")
        logging.info("%s 启动" % self.app_name)

    def stop(self):
        os.chdir("%s/bin" % self.tomcat_path)
        os.system("./shutdown.sh")
        logging.info("%s 停止" % self.app_name)

    def install(self, install_file):
        if self.is_running:
            logging.info("%s 安装失败，当前程序正在运行" % self.app_name)
            return
        if install_file[0:2] == "./":
            install_file = install_file[2:]
        shutil.copy(install_dir + os.sep + install_file, self._get_install_path() + os.sep)
        logging.info("%s 已安装" % self.app_name)

    def uninstall(self):
        os.system("rm -rf %s/*" % self._get_install_path())
        logging.info("%s 已卸载" % self.app_name)
