from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from orsun import loading
from time import sleep


# find id in search box to driver able click,send_key to it
def find_required(driver):
    loading.check(driver)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'x-form-trigger.x-form-trigger-default.x-form-search-trigger.x'
                                                   '-form-search-trigger-default.x-rtl'))
    )

    id = element.get_attribute('id')
    id = id[:id.find('id')+2]

    return id


# search lesson_code in site search box
def find(driver, lesson_code):
    search_box_xpath = f'//*[@id="{find_required(driver)}-inputEl"]'
    search = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, search_box_xpath))
    )

    # click on search box and clear filed then sleep 0.5 second
    loading.check(driver)
    # search.click()

    # clear search field
    search.clear()
    sleep(0.5)
    loading.check(driver)

    loading.is_ready_to_sendkeys(driver)

    # send_key lesson_code then sleep 0.5 second
    search.send_keys(lesson_code)
    sleep(0.5)
    loading.check(driver)


# Filter items found based on lesson code
def matching(driver, lesson_code):
    loading.check(driver)
    # List of items found that match the lesson code
    match = []

    items_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'x-grid-view.x-grid-with-col-lines.x-grid-with-row-lines.x-fit'
                                                       '-item.x-rtl.x-grid-view-default.x-unselectable.x-scroller')))

    items = WebDriverWait(items_box, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'table'))
    )

    for i in range(1, len(items) + 1):
        lesson_code_in_table_xpath = f'/html/body/div[5]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[2]' \
                               f'/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]' \
                               f'/table[{i}]/tbody/tr/td[3]/div'
        lesson_code_in_table = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, lesson_code_in_table_xpath)))

        if lesson_code in lesson_code_in_table.text:
            match.append({'row': i, 'webelement': items[i - 1]})

    # return lesson row id + selenium WebElement
    return match
