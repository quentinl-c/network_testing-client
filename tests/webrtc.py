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


class Writer(Collab):
    """docstring for Writer"""
    def __init__(self):
        Collab.__init__(self, 'ace_text-input')
        self.__word_to_type = "type_something"

    def run(self):
        print("=== Writer is starting ===")
        self.alive = True
        while self.alive:
            print("=== Writer is typing : %s ===" % self.__word_to_type)
            self.select.send_keys(self.__word_to_type)
            self.content_editor += self.__word_to_type
            time.sleep(5)

    def stop(self):
        Collab.stop(self)
        print("=== Writer is stopping ===")


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
    duration = 60
    delay = 15

    print("=== Duration : %s ===" % duration)
    print("=== Delay : %s ===" % delay)

    reader = Reader()
    writer = Writer()

    print("=== Experimentation is starting ===")
    reader.start()
    sleep(5)
    writer.start()

    time.sleep(duration)

    writer_content = writer.content_editor
    writer.stop()
    writer.join()

    time.sleep(delay)

    reader_content = reader.content_editor
    reader.stop()
    reader.join()

    print(writer_content)
    print(reader_content)
    print(len(writer_content))
    print(len(reader_content))
    assert (writer_content == reader_content), "reader and writer content don't match"
