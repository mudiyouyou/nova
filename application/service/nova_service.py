# coding=utf-8
import functools
import logging
from domain.app.service import app_service
from domain.host.service import host_service


def print_ip(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("当前主机:" + host_service.get_host_ip())
        result = func(*args, **kwargs)
        logging.info("当前主机:" + host_service.get_host_ip())
        return result

    return wrapper


@print_ip
def start(app_name):
    app_service.start(app_name)


@print_ip
def stop(app_name):
    app_service.stop(app_name)


@print_ip
def install(app_name, install_file):
    app_service.install(app_name, install_file)


@print_ip
def backup(app_name):
    app_service.backup(app_name)


@print_ip
def rollback(app_name):
    app_service.rollback(app_name)


@print_ip
def uninstall(app_name):
    app_service.uninstall(app_name)


@print_ip
def show_log(app_name, before_lines=100):
    app_service.show_log(app_name, before_lines)


def list_app():
    for app in app_service.list_app():
        logging.info("PID:%-10s 名称:%-30s CPU:%-10s 内存:%-10s" % (app.pid, app.app_name, app.cpu, app.memory))
