# coding=utf-8
import os

import psutil

from domain.app.entity import AppFactory
from infrastucture.setting import install_dir


def start(app_name):
    app = AppFactory.create(app_name)
    if app.is_installed():
        app.start()


def stop(app_name):
    app = AppFactory.create(app_name)
    if app.is_installed():
        app.stop()


def install(app_name, install_file):
    app = AppFactory.create(app_name, install_file)
    if app.is_installed():
        app.backup()
        app.stop()
        app.uninstall()
    app.install(install_file)


def backup(app_name):
    app = AppFactory.create(app_name)
    if app.is_installed():
        app.backup()


def rollback(app_name):
    app = AppFactory.create(app_name)
    app.rollback()


def uninstall(app_name):
    app = AppFactory.create(app_name)
    if app.is_installed():
        app.backup()
        app.stop()
        app.uninstall()


def show_log(app_name, before_lines):
    app = AppFactory.create(app_name)
    app.show_log(before_lines)


def list_app():
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
