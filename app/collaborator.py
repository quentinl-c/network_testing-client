import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
from logger import Logger


# Selenium
CHROME_LOCATION = "/usr/bin/google-chrome"


class Collaborator(threading.Thread):
    """docstring for Collaborator"""
    def __init__(self, url, selector, typing_speed):
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
        self.__display.quit()

    def saveMeasurement(self, role, *args):
        self.__results.bufferize(role, ' '.join(str(elt) for elt in args))

    def returnResults(self):
        return self.__results.genResult()
