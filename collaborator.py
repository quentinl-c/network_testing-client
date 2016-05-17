import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Selenium
REMOTE_DRIVER = 'http://127.0.0.1:4444/wd/hub'
SELECTOR = 'ace_text-input'


class Collaborator(threading.Thread):
    """docstring for Collaborator"""
    def __init__(self, client_id, rk, url):
        threading.Thread.__init__(self)
        print("New collab")
        self.client_id = client_id
        self.rk = rk
        self._driver = webdriver.Remote(
                command_executor=REMOTE_DRIVER,
                desired_capabilities=DesiredCapabilities.CHROME)
        self.__result_file = open(str(client_id) + '_' + str(rk), 'w')
        self._driver.get(url)
        self.select = None
        while self.select is None:
            print("YOOOLOOO")
            try:
                self.select = self.driver.find_element_by_class_name(
                    'ace_text-input')
            except Exception:
                continue
        print("TIITITITITI")

    def saveMeasurement(self, type, content, time_stamp):
        self.__writeInFile(type + ' ' + time_stamp + ' ' + content)

    def __writeInFile(self, measure):
        self.__result_file.write(measure)
