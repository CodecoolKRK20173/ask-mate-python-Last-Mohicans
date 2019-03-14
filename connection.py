import csv
import time


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
