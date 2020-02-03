# coding=utf-8
from datetime import datetime
import os
import shutil
import logging
from infrastucture.setting import backup_dir, install_dir, log_dir


class App(object):
    def __init__(self, app_name):
        self.app_name = app_name
        self.is_backup = False
        self.process = None

    @property
    def is_running(self):
        return self.process is not None

    @staticmethod
    def create_day_backup_dir():
        backup_today_path = backup_dir + os.sep + str(datetime.now().date())
        # 判断备份目录是否有当前日期目录
        if not os.path.exists(backup_today_path):
            os.mkdir(backup_today_path)
        return backup_today_path

    def is_installed(self):
        if os.path.exists("%s/%s" % (install_dir, self.app_name)):
            return True
        else:
            return False

    def get_today_app_backup_path(self):
        backup_today_path = self.create_day_backup_dir()
        backup_today_app_path = backup_today_path + os.sep + self.app_name
        return backup_today_app_path

    def backup(self):
        backup_today_app_path = self.get_today_app_backup_path()
        try:
            shutil.copytree(self._get_install_path(), backup_today_app_path)
        except Exception as e:
            pass
        logging.info("%s 已备份" % self.app_name)

    def rollback(self):
        # 判断当前程序是否在运行
        if self.is_running:
            logging.info("%s 回滚失败，当前程序正在运行" % self.app_name)
            return
        backup_today_app_path = self.get_today_app_backup_path()
        if not os.path.exists(backup_today_app_path):
            logging.info("%s 回滚失败，没有找到备份文件" % self.app_name)
            return
        if os.path.exists(self._get_install_path()):
            shutil.rmtree(self._get_install_path())
        shutil.copytree(backup_today_app_path, self._get_install_path())
        # 拷贝备份程序到程序目录
        logging.info("%s 已回滚" % self.app_name)

    def show_log(self, before_lines):
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = self.app_name + "-" + date_str + ".log"
        log_file_path = "%s/%s/%s" % (log_dir, self.app_name, log_file)
        if os.path.exists(log_file_path):
            os.system("tail -%sf %s" % (before_lines, log_file_path))
            return
        log_file_path = "%s/%s/%s" % (log_dir, self.app_name, "log_info.log")
        if os.path.exists(log_file_path):
            os.system("tail -%sf %s" % (before_lines, log_file_path))
            return
        logging.info("没有找到日志文件")

    def _get_install_path(self):
        pass

    @property
    def cpu(self):
        if self.process is not None:
            return round(self.process.cpu_percent(), 2)
        return "0"

    @property
    def memory(self):
        if self.process is not None:
            return str(round(self.process.memory_info().rss / 1024 / 1024, 0)) + "(MB)"
        return "0"
