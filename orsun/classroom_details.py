from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from persiantools import characters
from orsun import loading
import requests
import re

my_header = {
    "Host": "89.43.5.11:8082",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "*/*",
    "Referer": "http://89.43.5.11:8082/orsun/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": 'en-US,en;q=0.9'
}


def click(driver, item):
    details_button = f'/html/body/div[5]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div' \
                     f'/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/table[{item.get("row")}]' \
                     f'/tbody/tr/td[2]/div/img[1]'

    loading.check(driver)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, details_button))
    ).click()


def find_required(driver):
    loading.check(driver)

    bj_link = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '.x-panel-body.x-grid-with-col-lines.x-grid-with-row-lines'
                              '.x-grid-body.x-panel-body-default.x-panel-body-default.x-rtl'
                              '')))[1].get_attribute('id')

    bj_link = bj_link[:bj_link.find('_')]

    id_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
    ).get_attribute('id')
    id_link = id_link[id_link.find('_') + 1:]

    return {'id_link': id_link, 'bj_link': bj_link}


def details_data_creator(response):
    response = characters.ar_to_fa(response)
    response = response.replace('true', 'True')
    regex = re.compile(r"\"rows\":(\[.*])")
    classroom_details = eval(re.search(regex, response)[1])

    # for classroom data and time ('1401/03/12','14-15')
    classroom_details_list = []

    for item in classroom_details:
        classroom_details_list.append((item['2'], item['3']))

    return {'meetings': classroom_details_list}


def get_details_data(base_url, bj_and_id):
    url = f"{base_url}hyper_server.dll/HandleEvent?IsEvent=1&Obj={bj_and_id.get('bj_link')}" \
          f"&Evt=data&_S_ID={bj_and_id.get('id_link')}&options=1&page=1&start=0&limit=25"

    req = requests.get(url, headers=my_header)

    if req.ok:
        return details_data_creator(response=req.text)
    else:
        print(f'error in requests : {req.status_code}')


# for classroom name and teacher name
def classroom_info(driver, item):
    row = item.get('row')
    classroom_name = f'/html/body/div[5]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[2]/div[' \
                     f'2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/table[{row}]/tbody/tr/td[4]/div'

    teacher_fname = f'/html/body/div[5]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[2]/div[' \
                    f'2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/table[{row}]/tbody/tr/td[' \
                    f'5]/div'

    teacher_lname = f'/html/body/div[5]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[2]/div[' \
                    f'2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/table[{row}]/tbody/tr/td[' \
                    f'6]/div'

    classroom = characters.ar_to_fa(driver.find_element(By.XPATH, classroom_name).text)
    teacher = characters.ar_to_fa(driver.find_element(By.XPATH, teacher_fname).text + ' ' +
                                  driver.find_element(By.XPATH, teacher_lname).text)

    return {'classroom_name': classroom, 'teacher': teacher}


def get_details(driver, items, base_url):
    # all meetings fonded for classroom_code
    all_classrooms_meetings = []
    for item in items:
        classroom = {}

        classroom_and_teacher_name = classroom_info(driver, item)
        classroom.update(classroom_and_teacher_name)

        click(driver, item)
        loading.check(driver)

        meetings = get_details_data(base_url=base_url, bj_and_id=find_required(driver))
        classroom.update(meetings)

        all_classrooms_meetings.append(classroom)

        # close windows that show classroom meeting
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'x-tool-tool-el.x-tool-img.x-tool-close.x-rtl'))
        ).click()

    return all_classrooms_meetings
