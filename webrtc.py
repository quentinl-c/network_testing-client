""" WebRTC test :

"""
import threading
import random
import string
import time
from selenium import webdriver
from pyvirtualdisplay import Display

URL = "http://mute-collabedition.rhcloud.com/peer/doc/"
DOCID = ''.join(random.choice(string.lowercase) for i in range(10))


class Collab(threading.Thread):
    """docstring forCollab"""
    def __init__(self, selector):
        self.__display = Display(visible=0, size=(800, 600))
        self.__display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = CHROME_LOCATION
        self.__driver = webdriver.Chrome("/opt/selenium/chromedriver",
                                         chrome_options=chrome_options,
                                         service_args=["--verbose",
                                                       "--log-path=/home/log"])
        self.__driver.get(URL + DOC)
        self.select = None
        self.alive = False
        while self.select is None:
            self.__driver.implicitly_wait(20)
            self.select = self.__driver.find_element_by_class_name(
                selector)

    def stop(self):
        self.alive = False
        self.__driver.close()
        self.__display.quit()


class Writer(Collaborator):
    """docstring for Writer"""
    def __init__(self):
        Collaborator.__init__(self, 'ace_content')
        self.__word_to_type = "type_something"

    def run(self):
        self.alive = True
        while self.alive:
            print("=== Writer is typing : %s ===" % self.__word_to_type)
            self.select.send_keys(self.__word_to_type)
            time.sleep(5)


class Reader(Collaborator):
    """docstring for Reader"""
    def __init__(self):
        Collaborator.__init__(self, 'ace_content')

    def run(self):
        old_content_len = 0
        self.alive = True
        while self.alive:
            content = self.select.text.replace('\n', '').replace('\r', '')
            new_content_len = len(content)
            diff = new_content_len - old_content_len

            if diff >= self.typing_speed:
                last_index = new_content_len - (diff % self.typing_speed)
                content = content[old_content_len:last_index]
                old_content_len = last_index
                print("=== Reader is reading something : %s ===" % content)

if __name__ == '__main__':
    reader = Reader()
    writer = Writer()

    reader.start()
    writer.start()

    time.sleep(60)

    reader.stop()
    writer.stop()

    reader.join()
    writer.join()
