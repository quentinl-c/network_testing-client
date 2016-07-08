from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
import threading
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

IS_LOCAL_CONFIG = bool(os.getenv('IS_LOCAL_CONFIG', False))

# Selenium
CHROME_LOCATION = "/usr/bin/google-chrome"
CHROMEDRIVER_LOCATION = os.getenv('CHROMEDRIVER_LOCATION',
                                  "/opt/selenium/chromedriver")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = CHROME_LOCATION

d = DesiredCapabilities.CHROME
d['loggingPrefs'] = {"driver": "ALL", "server": "ALL", "browser": "ALL"}

service_args = ["--verbose"]


class Collaborator(threading.Thread):
    """docstring for Collaborator"""
    def __init__(self, controller, url):
        threading.Thread.__init__(self)
        self._controller = controller
        self._log_path = './%s' % self._controller.id
        print(self._log_path)

        service_args.append(''.join(("--log-path=", self._log_path)))
        if not IS_LOCAL_CONFIG:
            logger.debug('=== Deployment mode ===')
            self.__display = Display(visible=0, size=(800, 600))
            self.__display.start()
            self._driver = webdriver.Chrome(CHROMEDRIVER_LOCATION,
                                            chrome_options=chrome_options,
                                            desired_capabilities=d,
                                            service_args=service_args)
        else:
            logger.debug('=== Local mode ===')
            self._driver = webdriver.Chrome(CHROMEDRIVER_LOCATION,
                                            desired_capabilities=d,
                                            service_args=service_args)
        self._driver.get(url)
        self.alive = False

    def kill(self):
        logger.debug('=== Collaborator will be killed soon ===')
        self.alive = False
        self._driver.close()

        if not IS_LOCAL_CONFIG:
            self.__display.stop()

        self.join()

    def getResults(self):
        # Default behavior
        content = ''
        with open(self._log_path, 'r') as content_file:
            content = content_file.read()
        self._controller.sendResults(content)
