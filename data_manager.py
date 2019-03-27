import connection
from psycopg2 import sql


# returns questions (list of dictionaries)
@connection.connection_handler
def get_questions(cursor):
    cursor.execute(
        sql.SQL("select * from {table} ORDER BY {column} DESC").format(
            table=sql.Identifier('question'), column=sql.Identifier('submission_time'))
    )
    questions = cursor.fetchall()
    return questions


# returns question of given id (dictionary)
@connection.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute(
        sql.SQL("select * from {table} where {column} = {q_id}").format(
            table=sql.Identifier('question'), column=sql.Identifier('id'), q_id=sql.Literal(question_id))
    )
    questions = cursor.fetchall()
    return questions[0]


@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute(
        sql.SQL("select {question_id} from {table} where {id} = {a_id}").format(
            table=sql.Identifier('answer'), id=sql.Identifier('id'),
            question_id=sql.Identifier('question_id'), a_id=sql.Literal(answer_id))
    )
    questions = cursor.fetchall()
    return questions[0]['question_id']


# returns answers associated with question of given id (list of dictionaries)
@connection.connection_handler
def get_answers_by_question_id(cursor, question_id):
    cursor.execute(
        sql.SQL("select * from {table} where {question_id} = {given_id} ORDER BY {time} DESC").format(
            table=sql.Identifier('answer'), question_id=sql.Identifier('question_id'),
            time=sql.Identifier('submission_time'), given_id=sql.Literal(question_id))
    )
    answers = cursor.fetchall()
    return answers


# updates question of give id
def update_question(updated_question, id):
    questions = connection.import_data(connection.QUESTIONS_FILE)
    questions[id] = updated_question
    connection.export_data(questions, connection.QUESTIONS_FILE)


# updates view_number of question of given id
@connection.connection_handler
def update_question_view_number(cursor, question_id):
    cursor.execute(
        sql.SQL("update {table} set {view_number} = {view_number} + 1 where {question_id} = {given_id}").format(
            table=sql.Identifier('question'), question_id=sql.Identifier('id'),
            view_number=sql.Identifier('view_number'), given_id=sql.Literal(question_id))
    )


# updates vote_number of record from given table of given id by value (int)
@connection.connection_handler
def update_vote_number(cursor, table, question_id, value):
    cursor.execute(
        sql.SQL("update {table} set {vote_number} = {vote_number} + {value} where {id} = {given_id}").format(
            table=sql.Identifier(table), id=sql.Identifier('id'),
            vote_number=sql.Identifier('vote_number'), value=sql.Literal(value),
            given_id=sql.Literal(question_id))
    )


# updates vote_number of answer of given id by value (int), returns question_id
def update_answer_vote_number(id, value):
    answers = connection.import_data(connection.ANSWERS_FILE)
    answer = answers[id]
    answers[id]['vote_number'] = int(answer['vote_number']) + value
    connection.export_data(answers, connection.ANSWERS_FILE)
    return answer['question_id']


# adds new question consisting of given values (list) to data storage file
@connection.connection_handler
def add_question(cursor, values):
    columns = ['submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']

    query = sql.SQL("insert into {table} ({}) values ({})").format(
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(map(sql.Literal, values)),
        table=sql.Identifier('question')
    )
    cursor.execute(
        sql.SQL(query.as_string(cursor))
    )


# adds new answer consisting of given values (list) to data storage file
@connection.connection_handler
def add_answer(cursor, values):
    columns = ['submission_time', 'vote_number', 'question_id', 'message', 'image']

    query = sql.SQL("insert into {table} ({}) values ({})").format(
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(map(sql.Literal, values)),
        table=sql.Identifier('answer')
    )
    cursor.execute(
        sql.SQL(query.as_string(cursor))
    )


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


@connection.connection_handler
def get_mentor_names_by_first_name(cursor, first_name):
    # cursor.execute("""
    #                 SELECT first_name, last_name FROM mentors
    #                 WHERE first_name = %(f_n)s ORDER BY first_name;
    #                """,
    #                {'f_n': first_name})
    # names = cursor.fetchall()
    # return names

    cursor.execute(
        sql.SQL("select {col1}, {col2} from {table} ").
            format(col1=sql.Identifier('first_name'),
                   col2=sql.Identifier('last_name'),
                   table=sql.Identifier('mentors'))
    )
    names = cursor.fetchall()
    return names
