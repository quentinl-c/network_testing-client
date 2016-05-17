from collaborator import Collaborator
from random import randint
import time
import hashlib
import threading


class Writer(Collaborator):
    """docstring for Writer"""
    def __init__(self, client_id, rk, url, typing_speed):
        Collaborator.__init__(self, client_id, rk, url)
        self.typing_speed = typing_speed
        self.__can_typing = False
        self.__word_to_type = self.__gen_word_to_type()

    def __writeInDocument(self):
        while self.__can_typing:
            time_stamp = time.time()
            self.select.send_keys(self.__word_to_type + ' ')
            self.saveMeasurement('w', self.__word_to_type + ' ', time_stamp)
            time.sleep(1)

    def __gen_word_to_type(self):
        h = hashlib.sha256(self.client_id + self.rk).hexdigest()
        while len(h) < self.typing_speed:
            h = h + h
        index0 = randint(0, len(h) - self.typing_speed)
        self.__word_to_type = h[index0:index0 + typing_speed]

    def stop(self):
        self.__can_typing = False
        self.__writing_thread.join()
        self._driver.close()

    def run(self):
        self.__can_typing = True
        self.__writing_thread = threading.Thread(target=writeInDocument)
        self.__writing_thread.start()

        old_content_len = 0
        with self.__can_typing:
            content = select.text
            time_stamp = time.time()
            if len(content) != old_content_len:
                old_content_len = len(content)
                content = content[old_content_len:]
                self.saveMeasurement('r', content, time_stamp)
