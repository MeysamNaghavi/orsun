import sqlite3


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
