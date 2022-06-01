from selenium.webdriver.common.by import By
from orsun import loading


# find id in search box to driver able click,send_key to it
def find_required(driver):
    element = driver.find_element(By.CLASS_NAME, 'x-form-trigger.x-form-trigger-default.x-form-search-trigger.x-form'
                                                 '-search-trigger-default.x-rtl')

    id = element.get_attribute('id')
    id = id[:id.find('id')+2]

    return id


def find(driver, lesson_code):
    search_box_xpath = f'//*[@id="{find_required(driver)}-inputEl"]'
    search = driver.find_element(By.XPATH, search_box_xpath)

    # click on search box and clear filed
    search.click()
    search.clear()

    # sleep if loadings... appear
    loading.check(driver)

    # send_key lesson_code
    search.send_keys(lesson_code)

    loading.check(driver)
