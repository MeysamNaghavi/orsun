import sqlite3


# check value for lesson code, must all number + len 7
def check_user_entered(value):
    if value.isdigit() and len(value) == 7:
        return True
    else:
        return False


# get lesson meetings from db and return meetings row from meetings table
def get_meetings(lesson_code):
    with sqlite3.connect('database.db') as connections:
        cursor = connections.cursor()
        meeting = cursor.execute("SELECT meetings FROM meetings WHERE lesson_code=?", (lesson_code,)).fetchone()
        if meeting is None:
            return None
        else:
            return meeting[0]


def get_response(user_entered):
    if check_user_entered(user_entered):
        data = get_meetings(user_entered)
        if data is None:
            return None
        else:
            return eval(data)
    elif check_user_entered(user_entered) is False:
        return False
