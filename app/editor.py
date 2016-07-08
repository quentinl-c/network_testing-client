from collaborator import Collaborator
import logging
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

WRITER_SELECTOR = 'ace_text-input'
READER_SELECTOR = 'ace_content'
FILTER = '[Tracker]'


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
            while self.alive:
                time_stamp = time.time()
                self.select.send_keys(self.word_to_type)
                time.sleep(1)
            else:
                content = self.select.text

    def getResults(self):
        tmp = []
        with open(self._log_path, 'r') as content_file:
            for line in content_file:
                beg = line.find(FILTER)
                if beg != -1:
                    rec = line[beg:].split(',')[0].split('"')[0]
                    tmp.append(rec)
        content = '\n'.join(tmp)
        self._controller.sendResults(content)
