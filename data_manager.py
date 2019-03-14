import connection


# returns questions (dictionary of dictionaries)
def get_questions():
    return connection.import_data(connection.QUESTIONS_FILE)


# returns question of given id (dictionary)
def get_question_by_id(id):
    questions = connection.import_data(connection.QUESTIONS_FILE)
    return questions[id]


# returns answers associated with question of given id (dictionary of dictionaries)
def get_answers_by_question_id(id):
    data = connection.import_data(connection.ANSWERS_FILE)
    answers = {}

    for answer_id, answer in data.items():
        if answer['question_id'] == id:
            answers[answer_id] = answer

    return answers


# updates question of give id
def update_question(updated_question, id):
    questions = connection.import_data(connection.QUESTIONS_FILE)
    questions[id] = updated_question
    connection.export_data(questions, connection.QUESTIONS_FILE)


# updates view_number of question of given id
def update_question_view_number(id):
    questions = connection.import_data(connection.QUESTIONS_FILE)
    question = questions[id]
    questions[id]['view_number'] = int(question['view_number']) + 1
    connection.export_data(questions, connection.QUESTIONS_FILE)


# updates vote_number of question of given id by value (int)
def update_question_vote_number(id, value):
    questions = connection.import_data(connection.QUESTIONS_FILE)
    question = questions[id]
    questions[id]['vote_number'] = int(question['vote_number']) + value
    connection.export_data(questions, connection.QUESTIONS_FILE)


# updates vote_number of answer of given id by value (int), returns question_id
def update_answer_vote_number(id, value):
    answers = connection.import_data(connection.ANSWERS_FILE)
    answer = answers[id]
    answers[id]['vote_number'] = int(answer['vote_number']) + value
    connection.export_data(answers, connection.ANSWERS_FILE)
    return answer['question_id']


# adds new question consisting of given values (list) to data storage file
def add_question(values):
    added_question = dict(zip(connection.QUESTION_FIELDS, values))
    connection.append_data(added_question, connection.QUESTIONS_FILE)


# adds new answer consisting of given values (list) to data storage file
def add_answer(values):
    added_answer = dict(zip(connection.ANSWER_FIELDS, values))
    connection.append_data(added_answer, connection.ANSWERS_FILE)


# removes question of given id, and associated answers
def remove_question(id):
    # import questions
    # remove question
    # export modified questions
    questions = connection.import_data(connection.QUESTIONS_FILE)
    questions.pop(id, None)
    connection.export_data(questions, connection.QUESTIONS_FILE)
    # import answers and answers with questions_id
    # remove answers with questions_id from answers
    # export modified answers
    answers = connection.import_data(connection.ANSWERS_FILE)
    answers_with_question_id = get_answers_by_question_id(id)
    [answers.pop(k, None) for k in answers_with_question_id]
    connection.export_data(answers, connection.ANSWERS_FILE)


# removes answer of given id, and returns question_id
def remove_answer(id):
    # import answers
    # remove answer
    # export modified answers
    answers = connection.import_data(connection.ANSWERS_FILE)
    question_id = answers.pop(id, None)['question_id']
    connection.export_data(answers, connection.ANSWERS_FILE)
    return question_id


# saves given questions data (dictionary of dictionaries)
def export_questions(data):
    connection.export_data(data, connection.QUESTIONS_FILE)


# returns a list of fields for question
def get_question_fields():
    return connection.QUESTION_FIELDS


# returns new id for new question
def get_new_question_id():
    data = connection.import_data(connection.QUESTIONS_FILE)
    data = {int(key): value for key, value in data.items()}
    ids = sorted(data.keys())
    if ids:
        return str(int(ids[-1]) + 1)
    else:
        return 0


# eturns new id for new answer
def get_new_answer_id():
    data = connection.import_data(connection.ANSWERS_FILE)
    data = {int(key): value for key, value in data.items()}
    ids = sorted(data.keys())
    if ids:
        return str(int(ids[-1]) + 1)
    else:
        return 0
