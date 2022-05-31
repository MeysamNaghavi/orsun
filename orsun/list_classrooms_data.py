from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from persiantools import characters
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


# find bj and id,which are required for the request.get
def find_required(driver):
    # find bj in dom
    bj_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.x-panel.x-abs-layout-item.x-rtl.x-panel-default.x-grid'))
    ).get_attribute('id')
    bj_link = bj_link[:bj_link.find('_')]

    # find id in dom
    id_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
    ).get_attribute('id')
    id_link = id_link[id_link.find('_') + 1:]

    return {'bj_link': bj_link, 'id_link': id_link}


# create dict of classrooms data
def classrooms_data_creator(response):
    # convert response arabic alphabet to persian
    response = characters.ar_to_fa(response)

    # find where is start data
    regex = re.compile(r"\"rows\":(\[.*])")
    matches = eval(re.search(regex, response)[1])

    # Create useful personalized data from extracted information
    data = []
    for items in matches:
        lesson = {
                'lesson_code': items["1"],
                'lesson_name': items["2"],
                'teacher_fname': items["3"],
                'teacher_lname': items["4"],
                'teacher_mobile': items["5"],
                'degree': items["6"],
                'exam_type': items["7"],
                'city': items["8"],
                'description': items["9"]
            }
        data.append(lesson)

    return data


# for requests to get all classrooms data
def get_classrooms_data(driver, base_url):
    bj_and_id = find_required(driver)
    url = f'{base_url}hyper_server.dll/HandleEvent?IsEvent=1&Obj={bj_and_id["bj_link"]}' \
          f'&Evt=data&_S_ID={bj_and_id["id_link"]}&options=1&page=1&start=0&limit=25 '

    req = requests.get(url, headers=my_header)

    if req.ok:
        return classrooms_data_creator(response=req.text)
    else:
        print(f'error in requests : {req.status_code}')
