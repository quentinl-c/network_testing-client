from collaborator import Collaborator
import time


SELECTOR = 'ace_content'


class Reader(Collaborator):
    """docstring for Reader"""
    def __init__(self, client_id, rk, url, typing_speed):
        Collaborator.__init__(self, client_id, rk, url, SELECTOR, 'r')

    def run(self):
        old_content_len = 0
        while self.alive:
            content = self.select.text.replace('\n', '').replace('\r', '')

            time_stamp = time.time()
            new_content_len = len(content)
            diff = new_content_len - old_content_len

            if diff >= self.typing_speed:
                last_index = new_content_len - (diff % self.typing_speed)
                content = content[old_content_len:last_index]
                old_content_len = last_index
                self.saveMeasurement(time_stamp, content)
