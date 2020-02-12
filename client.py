# coding=utf-8
import logging
import sys

import command_interface

log_format = '%(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
if __name__ == "__main__":
    command_interface.command()
