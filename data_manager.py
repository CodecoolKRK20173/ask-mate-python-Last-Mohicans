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


# updates view_number of question by given id, and returns dictionary of questions
def update_question_view_number(id):
    questions = connection.import_data(connection.QUESTIONS_FILE)
    question = questions[id]
    questions[id]['view_number'] = int(question['view_number']) + 1
    connection.export_data(questions, connection.QUESTIONS_FILE)
    return  questions


def add_question(id, question):
    questions = connection.import_data(connection.QUESTIONS_FILE)
    questions[id] = question
    connection.export_data(questions, connection.QUESTIONS_FILE)


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
