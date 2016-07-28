from collaborator import Collaborator
import os
import random
import logging
import time

logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

HOME_DIR = os.getenv('HOME_DIR', '/home/')

WRITER_SELECTOR = 'ace_text-input'
READER_SELECTOR = 'ace_content'
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
            selector = WRITER_SELECTOR
            self.word_to_type = word_to_type
        else:
            selector = READER_SELECTOR
            self.word_to_type = None

        self.select = None
        while self.select is None:
            self._driver.implicitly_wait(20)
            self.select = self._driver.find_element_by_class_name(
                selector)

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
                self.select.send_keys(w)
                self.counter += 1
                time.sleep(2)
            else:
                content = self.select.text
        self.saveTxt()

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

    def saveTxt(self):
        if self.word_to_type is not None:
            self.select = None
            while self.select is None:
                self._driver.implicitly_wait(20)
                self.select = self._driver.find_element_by_class_name(
                    READER_SELECTOR)

        content = self.select.text
        file = open(HOME_DIR + str(self._controller.id) + '_content.txt', 'w')
        file.write(content)
        file.close()
