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
