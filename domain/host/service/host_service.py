# coding=utf-8

from domain.host.entity import AppFactory


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


def get_tail_of_log(app_name):
    app = AppFactory.create(app_name)
    return app.get_tail_of_log()
