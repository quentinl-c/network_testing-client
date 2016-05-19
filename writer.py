from collaborator import Collaborator
from random import randint
from logger import Logger
import time
import hashlib
import threading

SELECTOR = 'ace_text-input'


class Writer(Collaborator):
    """docstring for Writer"""
    def __init__(self, client_id, rk, url, typing_speed):
        Collaborator.__init__(self, client_id, rk, url, SELECTOR, 'w')
        self.typing_speed = typing_speed
        self.__word_to_type = "abcd|"

    def run(self):
        self.alive = True
        while self.alive:
            time_stamp = time.time()
            self.select.send_keys(self.__word_to_type)
            self.saveMeasurement(time_stamp, self.__word_to_type)
            time.sleep(1)
