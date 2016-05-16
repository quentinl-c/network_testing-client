import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Selenium
REMOTE_DRIVER = 'http://127.0.0.1:4444/wd/hub'
SELECTOR = 'ace_text-input'


class Collaborator(threading.Thread):
    """docstring for Collaborator"""
    def __init__(self, client_id, rg, url):
        threading.Thread.__init__(self)
        self._driver = webdriver.Remote(
                command_executor=REMOTE_DRIVER,
                desired_capabilities=DesiredCapabilities.CHROME)
        self.__result_file = open(client_id + '_' + rg, 'w')
        self._driver.get(url)
        while self.select is None:
            try:
                self.select = self.driver.find_element_by_class_name(
                    SELECTOR)
            except Exception:
                continue

    def saveMeasures(self, measure):
        self.__result_file.write(measure)
