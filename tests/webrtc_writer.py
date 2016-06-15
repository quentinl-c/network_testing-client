""" WebRTC test :

"""
import threading
import time
import sys
from selenium import webdriver
from pyvirtualdisplay import Display

CHROME_LOCATION = "/usr/bin/google-chrome"


class Collab(threading.Thread):
    """docstring forCollab"""
    def __init__(self, selector, url):
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
        self.__driver.get(url)
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
    def __init__(self, url):
        Collab.__init__(self, 'ace_text-input', url)
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

if __name__ == '__main__':
    duration = 60
    print("=== Uptime : %s ===" % duration)

    if len(sys.argv) < 2:
        sys.exit(1)

    url = sys.argv[1]
    print("=== URL : %s ===" % url)

    writer = Writer(url)
    writer.start()

    time.sleep(duration)

    writer_content = writer.content_editor
    writer.stop()
    writer.join()

    print("=== Content read ===")
    print(writer_content)
    print("=== Len : %s ===" % len(writer_content))
