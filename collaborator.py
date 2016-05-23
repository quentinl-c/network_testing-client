import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from logger import Logger


# Selenium
REMOTE_DRIVER = 'http://127.0.0.1:4444/wd/hub'


class Collaborator(threading.Thread):
    """docstring for Collaborator"""
    def __init__(self, url, selector, typing_speed):
        threading.Thread.__init__(self)
        self.__driver = webdriver.Remote(REMOTE_DRIVER,
                                         DesiredCapabilities.CHROME)
        self.__results = Logger()
        self.alive = False
        self.typing_speed = typing_speed
        self.__driver.get(url)

        self.select = None
        while self.select is None:
            self.__driver.implicitly_wait(20)
            self.select = self.__driver.find_element_by_class_name(
                selector)

    def stop(self):
        self.alive = False
        self.__driver.close()

    def saveMeasurement(self, role, *args):
        self.__results.bufferize(role, ' '.join(str(elt) for elt in args))

    def returnResults(self):
        return self.__results.genResult()
