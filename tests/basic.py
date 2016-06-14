""" Basic test :
This test only launches a Chrome browser and prints source code of
http://www.google.com
For more information about a potential issue, you can consult log in home
folder
"""
from selenium import webdriver
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 600))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = "/usr/bin/google-chrome"
driver = webdriver.Chrome("/opt/selenium/chromedriver",
                          chrome_options=chrome_options,
                          service_args=["--verbose", "--log-path=/home/log"])
driver.get("http://www.google.com")

print(driver.page_source.encode('utf-8'))

driver.quit()
display.stop()
