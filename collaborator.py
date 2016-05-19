import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from logger import Logger


# Selenium
REMOTE_DRIVER = 'http://127.0.0.1:4444/wd/hub'


class Collaborator(threading.Thread):
    """docstring for Collaborator"""
    def __init__(self, client_id, rk, url, selector, role):
        threading.Thread.__init__(self)
        self._client_id = client_id
        self._rk = rk
        self._driver = webdriver.Remote(
                command_executor=REMOTE_DRIVER,
                desired_capabilities=DesiredCapabilities.CHROME)
        self.__results = Logger(role)
        self.alive = False
        self.__driver.get(url)

        self.select = None
        while self.select is None:
            self._driver.implicitly_wait(20)
            self.select = self._driver.find_element_by_class_name(
                selector)

    def stop(self):
        self.alive = False
        self.__driver.close()

    def saveMeasurement(self, *args):
        self.__results.bufferize(' '.join(str(elt) for elt in args))

    def saveResults(self):
        # TODO : Send file to the server
        self.__result_file.saveBuffer()
        self.__result_file.saveFile()
