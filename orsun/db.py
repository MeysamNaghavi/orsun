import sqlite3
import json


def save_classrooms_db(data):
    with sqlite3.connect('database.db') as connections:

        cursor = connections.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS classrooms
                        (lesson_code text,
                        lesson_name text,
                        teacher_fname text,
                        teacher_lname text,
                        teacher_mobile text,
                        degree text,
                        exam_type text,
                        city text,
                        description text)
                        ''')

        cursor.executemany('INSERT INTO classrooms VALUES (:lesson_code ,:lesson_name ,:teacher_fname ,'
                           ':teacher_lname ,:teacher_mobile ,:degree ,:exam_type ,:city ,:description)', data)

    print("Database created successfully")


# save classroom details for one lesson_code in table meetings
def save_classroom_details(lesson_code, data):
    meetings_details = json.dumps(data, ensure_ascii=False)

    with sqlite3.connect('database.db') as connections:

        cursor = connections.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS meetings
                        (lesson_code text UNIQUE,
                        meetings text)
                        ''')

        cursor.execute('INSERT OR REPLACE INTO meetings VALUES (?, ?)', (lesson_code, meetings_details))


# create new table for perform search action, just have lessons_code which will be removed after a successful search
def lesson_codes_for_search():
    with sqlite3.connect('database.db') as connections:

        cursor = connections.cursor()

        all_lessons_code = cursor.execute('SELECT lesson_code FROM classrooms').fetchall()

        cursor.execute('''CREATE TABLE IF NOT EXISTS codes
                                (lesson_code text UNIQUE)
                                ''')

        cursor.executemany('INSERT OR REPLACE INTO codes VALUES (?)', all_lessons_code)


def remove_from_codes(lesson_code):
    with sqlite3.connect('database.db') as connections:

        cursor = connections.cursor()

        cursor.execute(f'DELETE FROM codes WHERE lesson_code = {lesson_code}')


# to get one lesson_code from table codes
def get_one_code():
    with sqlite3.connect('database.db') as connections:
        cursor = connections.cursor()

        code = cursor.execute('SELECT lesson_code FROM codes')

        return code.fetchone()


# return tables name in database
def get_tables_name():
    with sqlite3.connect('database.db') as connections:
        cursor = connections.cursor()

        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

        return tables.fetchall()