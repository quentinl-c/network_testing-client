from collaborator import Collaborator
from selenium import webdriver
import time
import threading


# Job
def writeInDocument(select, word):
    select.send_keys(word)
    time.wait(1)


class Writer(Collaborator):
    """docstring for Writer"""
    def __init__(self, typing_speed, webdriver=webdriver.Chrome(CHROMEDIRVER)):
        Collaborator.__init__(self,
                              webdriver=webdriver)
        self.select = None
        self.typing_speed = typing_speed
        self.can_typing = False
        while self.select is None:
            try:
                self.select = self.driver.find_element_by_class_name(
                    'ace_text-input')
            except Exception:
                continue

    def run(self):
        t = threading.Thread(target=writeInDocument(self.select, self.word))
        with True:

