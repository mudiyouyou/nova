import logging

from kazoo.client import KazooClient, KazooState

import setting


class ZClient:
    def __init__(self):
        self.__zk = KazooClient(hosts=setting.zoo_server)
        self.__zk.start()
        self.__app_on_host = None
        self.__ip = None

        @self.__zk.add_listener
        def client_func(state):
            if state == KazooState.CONNECTED:
                logging.info("已连接zookeeper")

    def init_agent(self, ip):
        self.__ip = ip
        self.register_agent_node()
        self.load_app_on_host()

    def register_agent_node(self):
        """注册Agent节点"""
        self.__zk.create("/nova/agent/" + self.__ip, ephemeral=True, makepath=True)
        logging.info("注册Agent节点")

    def load_app_on_host(self):
        """加载本主机安装列表并自动更新"""

        @self.__zk.DataWatch("/nova/host/" + self.__ip)
        def update(data, stat):
            self.__app_on_host = bytes.decode(data).split(",")
            logging.info("安装列表更新:%s" % self.__app_on_host)

    def get_app_on_host(self):
        return self.__app_on_host

    def add_app_to_cluster(self, app_name):
        self.__zk.ensure_path("/nova/cluster/" + app_name)
        self.__zk.create("/nova/cluster/" + app_name + "/" + self.__ip)
        logging.info("添加%s到集群" % app_name)

    def remove_app_from_cluster(self, app_name):
        self.__zk.ensure_path("/nova/cluster/" + app_name)
        self.__zk.delete("/nova/cluster/" + app_name + "/" + self.__ip)
        logging.info("删除%s从集群" % app_name)

    def add_app_on_host(self, app_name, ip):
        if self.__zk.exists("/nova/host/" + ip):
            value, stat = self.__zk.get("/nova/host/" + ip)
            ll = set(bytes.decode(value).split(","))
            ll.add(app_name)
            self.__zk.set("/nova/host/" + ip, ",".join(ll).encode())
        else:
            self.__zk.create("/nova/host/" + ip, app_name.encode())

    def remove_app_from_host(self, app_name, ip):
        self.__zk.ensure_path("/nova/host/" + ip)
        value, stat = self.__zk.get("/nova/host/" + ip)
        if value is None:
            self.__zk.set("/nova/host/" + ip, app_name.encode())
        else:
            ll = bytes.decode(value).split(",")
            ll = [a for a in ll if a != app_name]
            self.__zk.set("/nova/host/" + ip, ",".join(ll).encode())

    def get_cluster(self, app_name=None):
        cluster = dict()
        if app_name is None:
            apps = self.__zk.get_children("/nova/cluster")
            for app in apps:
                cluster[app] = self.__zk.get_children("/nova/cluster/" + app)
            return cluster
        else:
            cluster[app_name] = self.__zk.get_children("/nova/cluster/" + app_name)
            return cluster


if __name__ == '__main__':
    import time
    import sys

    log_format = '%(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
    c = ZClient()
    # c.init_agent("192.168.3.9")
    # logging.info(c.get_app_on_host())
    # logging.info(c.get_cluster())
    c.add_app_on_host("wireless-payment", "192.168.3.9")
    time.sleep(1000)
