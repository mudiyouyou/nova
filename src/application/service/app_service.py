# coding=utf-8

from domain.host.service import host_service


def start(app_name):
    host_service.start(app_name)


def stop(app_name):
    host_service.stop(app_name)


def install(app_name, install_file):
    host_service.install(app_name, install_file)


def backup(app_name):
    host_service.backup(app_name)


def rollback(app_name):
    host_service.rollback(app_name)


def uninstall(app_name):
    host_service.uninstall(app_name)


def get_tail_of_log(app_name):
    return host_service.get_tail_of_log(app_name)
