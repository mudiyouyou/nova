# coding=utf-8
import os

home_path = os.environ["HOME"]
setting = dict()
with open(home_path + os.path.sep + ".nova") as f:
    if not f.readable():
        raise RuntimeError("未找到HOME目录下的.nova配置文件")
    for line in f.readlines():
        kv = line.split("=")
        setting[kv[0]] = kv[1].strip().replace("\n", "")

install_dir = setting["install_dir"]
backup_dir = setting["backup_dir"]
tomcat_dir = setting["tomcat_dir"]
log_dir = setting["log_dir"]
