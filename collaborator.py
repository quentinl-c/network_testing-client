import threading
from selenium import webdriver
from selenium.webdriver.support.ui import Select

URL = "http://152.81.9.28:8080/peer/doc/zerezkfeza"
# URL = "https://docs.google.com/document/d/18zd6xh4uKT8NTaPoRndhONkJmT2Mo6-SLl1kYOp3G24/edit?usp=sharing"
CHROMEDIRVER = "./chromedriver"
result_writer = "default.txt"


class Collaborator(threading.Thread):
    """docstring for Collaborator"""
    def __init__(self, result_writer=result_writer, url=URL,
                 webdriver=webdriver.Chrome(CHROMEDIRVER)):
        threading.Thread.__init__(self)
        self.result_writer = result_writer
        self.url = url
        self.driver = webdriver
        self.driver.get(self.url)
