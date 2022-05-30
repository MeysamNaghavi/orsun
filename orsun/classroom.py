from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# get click and open 'لیست کلاس ها'
def get_classrooms_section(driver):
    # open 'کلاس های مجازی' folder from right side
    to_double_click_section1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[5]/div/div/div/div/div/div/div/div[4]/div[2]/div/div/div/div[2]/div/div['
                       '2]/div[1]/div[2]/table[1]/tbody/tr/td/div/span')
        )
    )
    ActionChains(driver).double_click(on_element=to_double_click_section1).perform()

    # open 'دانشجو' folde from right side
    to_double_click_section2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div/div/div/div/div[4]/div['
                                              '2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/table['
                                              '2]/tbody/tr/td/div/span')
                                   )
    )
    ActionChains(driver).double_click(on_element=to_double_click_section2).perform()

    # click on 'لیست کلاس ها' from right side
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div/div/div/div/div[4]/div['
                                              '2]/div/div/div/div[2]/div/div[2]/div[1]/div[2]/table['
                                              '3]/tbody/tr/td/div/span')
                                   )
    ).click()


def get_today_classrooms_section(driver):
    ...
