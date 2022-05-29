from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep

# base config
site_url = 'http://89.43.5.14:8082/orsun/'
driver = webdriver.Firefox()
