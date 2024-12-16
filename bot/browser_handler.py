import os
import logging
import json
import requests
from fake_headers import Headers
import undetected_chromedriver as uc
from fake_headers import Headers
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import (InvalidSessionIdException,
                                        NoSuchElementException,
                                        WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.ui as ui

OSNAME = "win"
logger = logging.getLogger(__name__)
header = Headers(
            browser="chrome",
            os=OSNAME,
            headers=True
        ).generate()
agent = header['User-Agent']


chromedriver_path = os.path.join(os.path.dirname(__file__), '..', 'drivers', 'chromedriver.exe')

class BrowserHandler:
    def __init__(self, config_path="config/settings.json",loginData_json="config/login_data.json",sites_json="config/sites.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        with open(loginData_json) as f:
            self.login_data = json.load(f)
        with open(sites_json) as f:
            self.sites = json.load(f)
        
        self.status = False
        self.driver = None
        
    def initialize(self):
        """Initialize the Chrome WebDriver"""
        options = uc.ChromeOptions()
        #prefs = {"profile.default_content_setting_values.notifications": 2}
        #options.add_experimental_option("prefs", prefs)
        options.binary_location = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        #options.add_argument("--disable-web-security")
        #options.add_argument('--log-level=3')
        options.add_argument('--window-size=900,1080')
        #options.add_experimental_option(
        #            "excludeSwitches", ["enable-automation", "enable-logging"])
        #options.add_experimental_option('useAutomationExtension', False)
        #options.add_argument(f'user-agent={agent}')
        options.add_argument('--user-data-dir=C:\\Users\\tufan\\AppData\\Local\\Google\\Chrome\\User Data');
        options.add_argument('--profile-directory=Profile 6');
        if self.config["browser"]["headless"]:
            options.add_argument('--headless')
        

        self.driver = uc.Chrome(executable_path=chromedriver_path,options=options)
        self.driver.implicitly_wait(self.config["browser"]["timeout"])
        self.status = True
        
    def get_real_url(self, url):
        """Follow redirects to get the final URL"""
        try:
            response = requests.head(url, allow_redirects=True)
            return response.url
        except Exception as e:
            logger.error(f"Error resolving URL: {str(e)}")
            return url
            
    def navigate(self, url):
        """Navigate to a specific URL"""
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            logger.error(f"Navigation error: {str(e)}")
            return False
            
    def find_and_input(self, selector, value, wait=True):
        """Find an element and input a value"""
        try:
            if wait:
                element = WebDriverWait(self.driver, self.config["browser"]["timeout"]).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
            else:
                element = self.driver.find_element(By.XPATH, selector)
                
            element.clear()
            element.send_keys(value)
            return True
        except Exception as e:
            logger.error(f"Input error: {str(e)}")
            return False
            
    def click(self, selector, wait=True):
        """Click an element"""
        try:
            if wait:
                element = WebDriverWait(self.driver, self.config["browser"]["timeout"]).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
            else:
                element = self.driver.find_element(By.XPATH, selector)
                
            element.click()
            return True
        except Exception as e:
            logger.error(f"Click error: {str(e)}")
            return False
            
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.status = False