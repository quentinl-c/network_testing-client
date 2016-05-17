from collaborator import Collaborator
import time


class Reader(Collaborator):
    """docstring for Reader"""
    def __init__(self, client_id, rk, url, typing_speed):
        Collaborator.__init__(self, client_id, rk, url)
        self.__can_reading = False

    def stop(self):
        self.__can_reading = False
        self._driver.close()

    def run(self):
        old_content_len = 0

        self.__can_reading = True
        while self.__can_reading:
            content = select.text
            time_stamp = time.time()
            if len(content) != old_content_len:
                old_content_len = len(content)
                content = content[old_content_len:]
                self.saveMeasurement('r', content, time_stamp)
