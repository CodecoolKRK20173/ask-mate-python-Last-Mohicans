import connection


def get_questions():
    return connection.import_data(connection.QUESTIONS_FILE)


def get_answers_by_question_id(id):
    data = connection.import_data(connection.ANSWERS_FILE)
    answers = {}

    for answer_id, answer in data.items():
        if answer['question_id'] == id:
            answers[answer_id] = answer

    return answers


# updates view_number of question of given id
def update_question_view_number(id):
    questions = connection.import_data(connection.QUESTIONS_FILE)
    question = questions[id]
    questions[id]['view_number'] = int(question['view_number']) + 1
    connection.export_data(questions, connection.QUESTIONS_FILE)


# updates vote_number of question of given id by value
def update_question_vote_number(id, value):
    questions = connection.import_data(connection.QUESTIONS_FILE)
    question = questions[id]
    questions[id]['vote_number'] = int(question['vote_number']) + value
    connection.export_data(questions, connection.QUESTIONS_FILE)


# updates vote_number of answer of given id by value, returns question_id
def update_answer_vote_number(id, value):
    answers = connection.import_data(connection.ANSWERS_FILE)
    answer = answers[id]
    answers[id]['vote_number'] = int(answer['vote_number']) + value
    connection.export_data(answers, connection.ANSWERS_FILE)
    return answer['question_id']


def add_question(values):
    added_question = dict(zip(connection.QUESTION_FIELDS, values))
    connection.append_data(added_question, connection.QUESTIONS_FILE)


def add_answer(values):
    added_answer = dict(zip(connection.ANSWER_FIELDS, values))
    connection.append_data(added_answer, connection.ANSWERS_FILE)


def export_questions(data):
    connection.export_data(data, connection.QUESTIONS_FILE)


def get_question_fields():
    return connection.QUESTION_FIELDS


def get_new_question_id():
    data = connection.import_data(connection.QUESTIONS_FILE)
    ids = sorted(data.keys())
    if ids:
        return str(int(ids[-1]) + 1)
    else:
        return 0


def get_new_answer_id():
    data = connection.import_data(connection.ANSWERS_FILE)
    ids = sorted(data.keys())
    if ids:
        return str(int(ids[-1]) + 1)
    else:
        return 0
