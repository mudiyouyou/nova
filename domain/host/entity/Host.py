import os
import re


class Host:
    def __init__(self, ip=None):
        regex = re.compile('\s+')
        result = os.popen("ifconfig|grep inet|grep -v inet6|grep -v 127.0.0.1")
        args = regex.split(result.readline())
        self._ip = args[2]

    @property
    def ip(self):
        return self._ip


if __name__ == '__main__':
    logging.info(Host().ip)
