from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep


# get len of table
def len_tables(driver):
    items_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, 'x-grid-view.x-grid-with-col-lines.x-grid-with-row-lines.x-fit'
                            '-item.x-rtl.x-grid-view-default.x-unselectable.x-scroller')))

    items = WebDriverWait(items_box, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'table'))
    )
    return len(items)


# Checks if 'loading...' is displayed, falls asleep
def check(driver):
    while True:
        loadings = driver.find_elements(By.CLASS_NAME, 'x-mask-msg-text.x-rtl')
        if len(loadings) != 1:
            sleep(1)
        else:
            break


# check table of classrooms is updated or not
def is_table_update(driver):
    while True:
        if len_tables(driver) > 20:
            sleep(1)
        else:
            break


# check the effect of deleting the amount that should have been searched
def is_ready_to_sendkeys(driver):
    while True:
        if len_tables(driver) > 20:
            break
        else:
            sleep(1)
