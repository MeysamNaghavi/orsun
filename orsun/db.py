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

