from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


# check loading class count if is == 1 then continue
def check(driver):
    while True:
        loadings = driver.find_elements(By.CLASS_NAME, 'x-mask-msg-text.x-rtl')
        if len(loadings) != 1:
            sleep(1)
        else:
            break
