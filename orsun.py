from time import sleep
from selenium.common import NoSuchElementException, StaleElementReferenceException
from auth import login
from orsun import classroom, list_classrooms_data
from orsun import db
from orsun import loading, search
from orsun import classroom_details
from selenium import webdriver

config = {
    'password': None,
    'username': None,
    'site_url': 'http://89.43.5.10/orsun/',
    'tables_name': db.get_tables_name(),
}

driver = webdriver.Firefox()
driver.minimize_window()
driver.get(config['site_url'])
sleep(3)
login.do_login(driver=driver, username=config.get('username'), password=config.get('password'))
loading.check(driver)
classroom.get_classrooms_section(driver)


# reload and login then go today classrooms section
def refresh_process(lesson_code):
    driver.refresh()
    sleep(3)
    login.do_login(driver=driver, username=config.get('username'), password=config.get('password'))
    config['is_login'] = True

    loading.check(driver)

    classroom.get_classrooms_section(driver)

    loading.check(driver)

    search.find(driver, lesson_code)

    loading.check(driver)

    match = search.matching(driver, lesson_code)

    loading.check(driver)

    classroom_details_list = classroom_details.get_details(driver, match, config['site_url'])

    return classroom_details_list


# save all classrooms data in 'لیست کلاس های امروز'
def save_all_classrooms_to_db(driver):
    loading.check(driver)

    classroom.get_classrooms_section(driver)

    loading.is_ready_to_sendkeys(driver)

    # save classrooms data to database
    data = list_classrooms_data.get_classrooms_data(driver=driver, base_url=config['site_url'])
    db.save_classrooms_db(data)

    # update tables name config
    config['tables_name'] = db.get_tables_name()

    print(f'{len(data)} classrooms saved!\n')


# save details of all lesson codes available in the database.
def save_all_classrooms_details_to_db(driver):
    if 'codes' not in config.get('tables_name'):
        if 'classrooms' not in config.get('tables_name'):
            save_all_classrooms_to_db(driver)
            config['tables_name'] = db.get_tables_name()

        db.lesson_codes_for_search()
        config['tables_name'] = db.get_tables_name()
        driver.refresh()
        sleep(3)
        login.do_login(driver=driver, username=config.get('username'), password=config.get('password'))
        loading.check(driver)
        classroom.get_classrooms_section(driver)

    saved_cunt = 0
    while True:
        loading.check(driver)
        lesson_code = db.get_one_code()
        if lesson_code is not None:
            lesson_code = lesson_code[0]
            loading.check(driver)
            search.find(driver, lesson_code)

            loading.is_table_update(driver)
            loading.check(driver)

            match = search.matching(driver, lesson_code)

            loading.check(driver)
            try:
                classroom_details_list = classroom_details.get_details(driver, match, config['site_url'])
            except NoSuchElementException or StaleElementReferenceException:
                print('refresh_process\n')
                classroom_details_list = refresh_process(lesson_code)

            loading.check(driver)

            db.save_classroom_details(lesson_code, classroom_details_list)

            # after save need remove lesson_code from code table
            db.remove_from_codes(lesson_code)

            saved_cunt += 1

        else:
            if saved_cunt == 0:
                print('nothing to find and saved ! \n')
                exit()
            else:
                print(f'{saved_cunt} classrooms details saved in database')
                exit()


# search custom
def custom_search_and_save(classrooms_code):
    search_list = classrooms_code.split(',')
    search_list = [code for code in search_list if len(code) == 7]

    print(f'search and save valid lesson_code : {search_list}\n')
    saved_cunt = 0
    while len(search_list) != 0:
        lesson_code = search_list[0]
        loading.check(driver)
        search.find(driver, lesson_code)

        loading.is_table_update(driver)
        loading.check(driver)

        match = search.matching(driver, lesson_code)

        loading.check(driver)
        try:
            classroom_details_list = classroom_details.get_details(driver, match, config['site_url'])
        except NoSuchElementException or StaleElementReferenceException:
            print('refresh_process\n')
            classroom_details_list = refresh_process(lesson_code)

        loading.check(driver)

        db.save_classroom_details(lesson_code, classroom_details_list)

        search_list.remove(lesson_code)
        saved_cunt += 1

    print(f'{saved_cunt} classrooms details saved in database')

# 1 for save_all_classrooms_to_db
# 2 for save_all_classrooms_details_to_db
# 3 for custom_search_and_save
# 4 for exit

print('''
\t*** select ***
1 - save_all_classrooms_to_db
2 - save_all_classrooms_details_to_db
3 - custom_search_and_save
4 - exit
''')

what_is_do = input('Enter : ')

if what_is_do == '1':
    save_all_classrooms_to_db(driver)
elif what_is_do == '2':
    driver.minimize_window()
    save_all_classrooms_details_to_db(driver)
elif what_is_do == '3':
    codes = input("\nenter codes for custom search like 1,2,3 : ")
    custom_search_and_save(codes)
elif what_is_do == '4':
    exit()
else:
    print('Error')
