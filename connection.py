import csv
import time

import os
import psycopg2
import psycopg2.extras


QUESTION_FIELDS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_FIELDS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

QUESTIONS_FILE = './sample_data/question.csv'
ANSWERS_FILE = './sample_data/answer.csv'
UPLOAD_FOLDER = './static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def export_data(data_base, file):
    if file == QUESTIONS_FILE:
        fields = QUESTION_FIELDS
    elif file == ANSWERS_FILE:
        fields = ANSWER_FIELDS
    else:
        return False

    with open(file, "w") as f:

        writer = csv.DictWriter(f, fields)
        writer.writeheader()
        for key, val in sorted(data_base.items()):
            val['submission_time'] = int(time.mktime(val['submission_time']))
            row = {'id': key}
            row.update(val)
            writer.writerow(row)
    return True


# try ecxcept do kazdej z metod by sie przydal
# rozbić na 3 funkcje
def import_data(file):
    dictionary = {}
    rows = []
    index = 0

    if file == QUESTIONS_FILE:
        fields = QUESTION_FIELDS
    elif file == ANSWERS_FILE:
        fields = ANSWER_FIELDS
    else:
        return dictionary

    with open(file, "r") as f:
        reader = csv.reader(f)

        for line in reader:
            if index > 0:
                rows.append(line)
            index += 1

    for row in rows:
        if row:
            for i, field in enumerate(fields):
                if field == 'id':
                    dictionary[row[0]] = {}
                else:
                    if field == 'submission_time':
                        dictionary[row[0]][field] = time.localtime(int(row[i]))
                    else:
                        dictionary[row[0]][field] = row[i]

    return dictionary


def append_data(data, file):
    if file == QUESTIONS_FILE:
        fields = QUESTION_FIELDS
    elif file == ANSWERS_FILE:
        fields = ANSWER_FIELDS
    else:
        return False

    with open(file, 'a') as f:
        writer = csv.DictWriter(f, fields)
        writer.writerow(data)
    return True



#nowa część


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper


