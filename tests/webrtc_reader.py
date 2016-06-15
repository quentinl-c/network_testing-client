""" WebRTC test :

"""
import threading
import random
import string
import time
from selenium import webdriver
from pyvirtualdisplay import Display

URL = "http://mute-collabedition.rhcloud.com/peer/doc/"
DOCID = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
CHROME_LOCATION = "/usr/bin/google-chrome"


class Collab(threading.Thread):
    """docstring forCollab"""
    def __init__(self, selector):
        threading.Thread.__init__(self)
        self.__display = Display(visible=0, size=(800, 600))
        self.__display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = CHROME_LOCATION
        self.__driver = webdriver.Chrome("/opt/selenium/chromedriver",
                                         chrome_options=chrome_options,
                                         service_args=["--verbose",
                                                       "--log-path=/home/log"])
        self.__driver.get(URL + DOCID)
        self.content_editor = ""
        self.alive = False
        self.select = None
        while self.select is None:
            self.__driver.implicitly_wait(20)
            self.select = self.__driver.find_element_by_class_name(
                selector)

    def stop(self):
        self.alive = False
        self.__driver.close()
        self.__display.stop()


class Reader(Collab):
    """docstring for Reader"""
    def __init__(self):
        Collab.__init__(self, 'ace_content')

    def run(self):
        print("=== Reader is starting ===")
        old_content_len = 0
        self.alive = True
        while self.alive:
            content = self.select.text.replace('\n', '').replace('\r', '')
            new_content_len = len(content)
            diff = new_content_len - old_content_len

            if diff > 0:
                last_index = new_content_len
                content = content[old_content_len:last_index]
                self.content_editor += content
                old_content_len = last_index
                print("=== Reader is reading something : %s ===" % content)
            time.sleep(1)

        def stop(self):
            Collab.stop(self)
            print("=== Reader is stopping ===")

if __name__ == '__main__':
    duration = 180
    url = URL + DOCID
    print("=== URL : %s ===" % url)
    print("=== Uptime : %s ===" % duration)

    reader = Reader()
    reader.start()

    time.sleep(duration)

    reader_content = reader.content_editor
    reader.stop()
    reader.join()

    print("=== Content read ===")
    print(reader_content)
    print("=== Len : %s ===" % len(reader_content))
