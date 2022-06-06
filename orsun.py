from selenium import webdriver
from auth import login
from orsun import classroom, list_classrooms_data
from orsun import db
from orsun import loading, search
from orsun import classroom_details
from selenium import webdriver

config = {
    'password': None,
    'username': None,
    'is_classrooms_table_created': False,
    'is_login': False,
    'site_url': 'http://89.43.5.10/orsun/',
    'tables_name': db.get_tables_name(),
}

# set driver executable_path if not  find
driver = webdriver.Firefox()
driver.minimize_window()

if config.get('username') or config.get('password') is None:
    config['username'] = input('Enter Username : ')
    config['password'] = input('Enter Password : ')


def refresh_process(lesson_code):
    driver.refresh()

    loading.check(driver)

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
def save_all_classrooms_to_db():
    if config['is_login'] is not True:
        driver.get(config['site_url'])
        login.do_login(driver=driver, username=config.get('username'), password=config.get('password'))
        config['is_login'] = True

    # save classrooms data to database
    data = list_classrooms_data.get_classrooms_data(driver=driver, base_url=config['site_url'])
    db.save_classrooms_db(data)

    # update tables name config
    config['tables_name'] = db.get_tables_name()

    print(f'{len(data)} classrooms saved!\n')


# save details of all lesson codes available in the database.
def save_all_classrooms_details_to_db():
    if 'classrooms' not in config.get('tables_name'):
        save_all_classrooms_to_db()
        db.lesson_codes_for_search()
        config['tables_name'] = db.get_tables_name()

    if 'code' not in config.get('code'):
        db.lesson_codes_for_search()
        config['tables_name'] = db.get_tables_name()

    saved_cunt = 0
    while True:
        loading.check(driver)
        lesson_code = db.get_one_code()

        if type(lesson_code) is not None:
            lesson_code = lesson_code[0]
            search.find(driver, lesson_code)

            loading.check(driver)

            match = search.matching(driver, lesson_code)

            loading.check(driver)
            try:
                classroom_details_list = classroom_details.get_details(driver, match, config['site_url'])
            except:
                refresh_process(lesson_code)

            loading.check(driver)

            db.save_classroom_details(lesson_code, classroom_details_list)

            # after save need remove lesson_code from code table
            db.remove_from_codes(lesson_code)

            saved_cunt += 1

        else:
            if saved_cunt == 0:
                print('nothing to find and saved ! \n')
                break
            else:
                print(f'{saved_cunt} classrooms details saved in database')
                break



