from collaborator import Collaborator
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
import logging
import time

logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

HOME_DIR = os.getenv('HOME_DIR', '/home/')

TEXT_AREA = 'textarea'
BUTTON = 'button'
FILTER = '[Tracker]'
tempo = 15  # Client will wait 20 secondes befores getting results


class Editor(Collaborator):
    """docstring for Editor"""
    def __init__(self, controller, target, typing_speed, word_to_type):
        Collaborator.__init__(self, controller, target)
        logger.debug("===  Editor is being instanciated ===")
        self.word_to_type = None
        self.counter = 0

        if len(word_to_type) > 0:
            self.word_to_type = word_to_type

        self.text_area = None
        while self.text_area is None:
            self._driver.implicitly_wait(20)
            self.text_area = self._driver.find_elements_by_id(TEXT_AREA)
            print(self.text_area)
        self.button = None
        while self.button is None:
            self._driver.implicitly_wait(20)
            self.button = self._driver.find_elements_by_id(BUTTON)
        print(self.button)

    def run(self):
        self.alive = True
        if self.word_to_type is not None:
            beg_time = random.uniform(2.0, 6.0)
            time.sleep(beg_time)

        while self.alive:
            if self.word_to_type is not None:
                time_stamp = time.time()
                w = ''.join((self.word_to_type, ';',
                             str(self.counter).zfill(6)))
                self.text_area[0].send_keys(w)
                self.button[0].click()
                self.counter += 1
                time.sleep(2)
            else:
                content = self.text_area[0].text

    def getResults(self):
        time.sleep(tempo)
        logger.debug("=== Get results from log files ===")
        tmp = []
        self.alive = False
        time.sleep(tempo)
        with open(self._log_path, 'r') as content_file:
            for line in content_file:
                beg = line.find(FILTER)
                if beg != -1:
                    rec = line[beg:].split(',')[0].split('"')[0]
                    tmp.append(rec)
        content = '\n'.join(tmp)
        self._controller.sendResults(content)
