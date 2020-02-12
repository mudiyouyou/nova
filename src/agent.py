# coding=utf-8

import logging
import sys

from setting import log_dir
from interface import web_interface

log_format = '%(message)s'
# logging.basicConfig(filename=log_dir + os.path.sep + 'nova.log', level=logging.DEBUG, format=log_format)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
if __name__ == "__main__":
    web_interface.start(port=9090)


