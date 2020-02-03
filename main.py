# coding=utf-8

from interface import nova_interface
import logging
import sys

log_format = '%(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
if __name__ == "__main__":
    nova_interface.command()
