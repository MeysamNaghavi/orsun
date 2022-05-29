from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from time import sleep

# base config
site_url = 'http://89.43.5.14:8082/orsun/'
driver = webdriver.Firefox()


def login(url, username, password):
    driver.get(url)

    # fill username filed
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="O17_id-inputEl"]'))
    ).send_keys(username)

    # fill password filed
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="O1B_id-inputEl"]'))
    ).send_keys(password)

    # fill captcha filed
    captcha = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="O37_id_td"]'))
    ).text
    captcha = list(captcha)
    captcha = eval(f"{captcha[1]}{captcha[2]}{captcha[3]}")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="O3F_id-inputEl"]'))
    ).send_keys(captcha)

    # click on 'ورود'
    try:
        driver.find_element(By.XPATH, '//*[@id="O4F_id-btnEl"]').click()
    except ElementClickInterceptedException:
        sleep(2)
        driver.find_element(By.XPATH, '//*[@id="O4F_id-btnEl"]').click()
