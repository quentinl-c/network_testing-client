from collaborator import Collaborator
import random
import logging
import time

logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

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

        if len(word_to_type) > 0:
            selctor = WRITER_SELECTOR
        else:
            selctor = READER_SELECTOR

        self.word_to_type = word_to_type
        self.select = None
        while self.select is None:
            self._driver.implicitly_wait(20)
            self.select = self._driver.find_element_by_class_name(
                WRITER_SELECTOR)

    def run(self):
        self.alive = True

        if self.word_to_type is not None:
            beg_time = random.uniform(2.0, 6.0)
            time.sleep(beg_time)

        while self.alive:
            if self.word_to_type is not None:
                time_stamp = time.time()
                self.select.send_keys(self.word_to_type)
                time.sleep(2)
            else:
                content = self.select.text
        print(self.select.text)

    def getResults(self):
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
