import logging
import os
import re
from threading import Timer

import psutil

from host.entity import AppFactory
from infrastucture.setting import install_dir
from zoo_client import ZClient


class Host:
    def __init__(self):
        self.__ip = Host.get_ip()
        self.__zclient = ZClient()
        self.__zclient.init_agent(self.__ip)

    @staticmethod
    def get_ip():
        regex = re.compile('\s+')
        result = os.popen("ifconfig|grep inet|grep -v inet6|grep -v 127.0.0.1")
        args = regex.split(result.readline())
        return args[2]

    def start_monitor(self):
        def sync_app_online():
            apps_online = set([app.app_name for app in Host.list_online()])
            apps_cluster = self.__zclient.get_cluster()
            apps_old = set()
            for k in apps_cluster:
                if self.__ip in apps_cluster[k]:
                    apps_old.add(k)
            apps_added = apps_online - apps_old
            apps_removed = apps_old - apps_online
            for app1 in apps_added:
                self.__zclient.add_app_to_cluster(app1)
            for app1 in apps_removed:
                self.__zclient.remove_app_from_cluster(app1)
            timer = Timer(5, sync_app_online)
            timer.setDaemon(True)
            timer.start()

        timer = Timer(5, sync_app_online)
        timer.setDaemon(True)
        timer.start()

    def stop_monitor(self):
        self.__timer.stop()

    @staticmethod
    def list_online():
        app_list = dict()
        for d in os.listdir(install_dir):
            if os.path.isdir(install_dir + os.path.sep + d) and d.find("wireless") != -1:
                app_list[d] = AppFactory.create(d)
        for pid in psutil.pids():
            try:
                process = psutil.Process(pid)
                cwd = process.cwd()
            except Exception:
                continue
            if process.exe().find("java") is not -1:
                for app_name in app_list.keys():
                    if cwd.find(app_name) != -1:
                        app_list[app_name].process = process
        running_app_list = [app for app in app_list.values() if app.is_running is True]
        return running_app_list


if __name__ == '__main__':
    import sys

    log_format = '%(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
    host = Host()
    host.start_monitor()
