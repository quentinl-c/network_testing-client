#!/usr/bin/env python3
from controller import Controller
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Client(object):
    """docstring for Client"""
    def __init__(self):
        self.__controller = Controller()

    def launch(self):
        self.__controller.launchClient()

if __name__ == '__main__':
    logger.debug("=== Client is being launch ===")
    cli = Client()
    cli.launch()
