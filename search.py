from sqlalchemy import true
import creds
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time


#from selenium import webdrive

class Driver:
  def __init__(self):
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        #options.add_argument("--no-sandbox")
        #options.add_argument('--disable-dev-shm-usage')
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'}
        loginurl=('https://vtgems.com/#/login')
        secureurl=('https://vtgems.com/#/signup')
        #"driver_file_path is a placeholder for where to store chrome web driver, make sure to dowload Chrome driver version 97"
        self.driver = webdriver.Chrome("driver_file_path",options=options)
        self.driver.get(loginurl)
        username = self.driver.find_elements_by_xpath('//div[@class="login-input"]')
        user = username[0].find_element_by_xpath('//input[@class="ui-inputtext ui-corner-all ui-state-default ui-widget"]')
        passw = self.driver.find_element_by_xpath('//input[@type="password"]')
        user.send_keys(creds.USER)
        passw.send_keys(creds.PASS)
        self.driver.find_element_by_xpath('//span[@class="ui-button-text ui-clickable"]').click()
        self.driver.get(secureurl)


  def search(self):
    self.driver.implicitly_wait(3)
    b = self.driver.find_elements_by_tag_name('h3')
    return b
  
  def get_unfilled(self):
    waitlisted = []
    events = []
    unfilled = []
    driver = self.driver
    driver.refresh()
    b = driver.find_elements_by_xpath('//div[@class="p-col-12 p-lg-4 p-md-12 p-sm-12 item-detail"]/span')
    for link in b:
      print(link.text)
      if link.text.__contains__("Waitlisted"):
        waitlisted.append(link.text[:link.text.index(" Waitlisted")])

    c = driver.find_elements_by_tag_name('h3')
    for link in c:
        print(link.text)
        events.append(link.text)
    for i in range(len(waitlisted)):
        print(waitlisted[i])
        if int(waitlisted[i]) == 0:
              unfilled.append(events[i])
              print(events[i])
    return unfilled
      
  def send_link(self, result_links, search_words): 
    send_link = set()
    for link in result_links:
        text = link.text.lower()
        if search_words in text:  
          send_link.add(link.get('href'))
    return send_link