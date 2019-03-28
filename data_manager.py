import connection
from psycopg2 import sql


# returns questions (list of dictionaries)
def get_questions():
    return get_records_from_table('question', 'submission_time')


# returns comments (list of dictionaries)
def get_comments():
    return get_records_from_table('comment', 'submission_time')


# returns records from table
@connection.connection_handler
def get_records_from_table(cursor, table, order=''):
    ordered = ''
    if order:
        ordered = 'ORDER BY {column} DESC'
    cursor.execute(

        sql.SQL("select * from {table}"+ordered).format(
            table=sql.Identifier(table), column=sql.Identifier(order))

    )
    records = cursor.fetchall()
    return records


@connection.connection_handler
def get_questions_by_phrase(cursor, search_phrase):
    cursor.execute(

        sql.SQL("select {table_q}.* from {table_q} "
                "LEFT JOIN {table_a} on {table_a}.{question_id_fk}={table_q}.{question_id_pk} "
                "where {table_q}.{search_title} like {phrase} "
                "or {table_q}.{search_message} like {phrase} "
                "or {table_a}.{search_message} like {phrase}"
                "ORDER BY {table_q}.{column} DESC").format(
            table_q=sql.Identifier('question'),
            table_a=sql.Identifier('answer'),
            search_title=sql.Identifier('title'),
            search_message=sql.Identifier('message'),
            # search_message_a=sql.Identifier('message'),
            question_id_pk=sql.Identifier('id'),
            question_id_fk=sql.Identifier('question_id'),
            phrase=sql.Literal(search_phrase),
            column=sql.Identifier('submission_time'))

    )
    questions = cursor.fetchall()
    return questions


# returns question of given id (dictionary)
def get_question_by_id(question_id):
    return get_record('question', question_id)


# returns answer of given id (dictionary)
def get_answer_by_id(answer_id):
    return get_record('answer', answer_id)


# returns comment of given id (dictionary)
def get_comment_by_id(comment_id):
    return get_record('comment', comment_id)


# returns record of given id from table (dictionary)
@connection.connection_handler
def get_record(cursor, table, id_):
    cursor.execute(
        sql.SQL("select * from {table} where {column} = {q_id}").format(
            table=sql.Identifier(table), column=sql.Identifier('id'), q_id=sql.Literal(id_))
    )
    records = cursor.fetchall()
    return records[0]


# returns question_id from answer with given id
def get_question_id_by_answer_id(answer_id):
    return get_question_id_by_record_id_from_table('answer', answer_id)


# returns question_id from comment with given id
def get_question_id_by_comment_id(comment_id):
    return get_question_id_by_record_id_from_table('comment', comment_id)


@connection.connection_handler
def get_question_id_by_record_id_from_table(cursor, table, id_):
    cursor.execute(
        sql.SQL("select {question_id} from {table} where {id} = {given_id}").format(
            table=sql.Identifier(table), id=sql.Identifier('id'),
            question_id=sql.Identifier('question_id'), given_id=sql.Literal(id_))
    )
    records = cursor.fetchall()
    return records[0]['question_id']


# returns answers associated with question of given id (list of dictionaries)
def get_answers_by_question_id(question_id):
    return get_records_by_foreign_id('answer', 'question_id', question_id)


# returns records from table with id_type equal to id_ (list of dictionaries)
@connection.connection_handler
def get_records_by_foreign_id(cursor, table, id_type, id_):
    cursor.execute(
        sql.SQL("select * from {table} where {foreign_id} = {given_id} ORDER BY {time} DESC").format(
            table=sql.Identifier(table), foreign_id=sql.Identifier(id_type),
            time=sql.Identifier('submission_time'), given_id=sql.Literal(id_))
    )
    records = cursor.fetchall()
    return records


def update_question(values):
    columns = ['title', 'message', 'image']
    update_table('question', columns, values)


def update_answer(values):
    columns = ['message', 'image']
    update_table('answer', columns, values)


def update_comment(values):
    columns = ['message', 'edited_count']
    update_table('comment', columns, values)


# updates information in columns of table by values
@connection.connection_handler
def update_table(cursor, table, columns, values):

    query = sql.SQL("update {table} set ({column}) = ({value}) where id = {q_id}").format(
            table=sql.Identifier(table),
            column=sql.SQL(', ').join(map(sql.Identifier, columns)),
            value=sql.SQL(', ').join(map(sql.Literal, values[1:])),
            q_id=sql.Literal(values[0]))

    cursor.execute(
        sql.SQL(query.as_string(cursor))
    )


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


# adds new question consisting of given values (list) to data storage file
def add_question(values):
    columns = ['submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    insert_record('question', columns, values)


# adds new answer consisting of given values (list) to data storage file
def add_answer(values):
    columns = ['submission_time', 'vote_number', 'question_id', 'message', 'image']
    insert_record('answer', columns, values)


# adds new comment consisting of given values (list) to data storage file
def add_comment(values):
    columns = ['question_id', 'answer_id', 'message', 'submission_time', 'edited_count']
    insert_record('comment', columns, values)


# insert new record into table with values of columns
@connection.connection_handler
def insert_record(cursor, table, columns, values):
    query = sql.SQL("insert into {table} ({}) values ({})").format(
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(map(sql.Literal, values)),
        table=sql.Identifier(table)
    )
    cursor.execute(
        sql.SQL(query.as_string(cursor))
    )


# removes question of given id, and associated answers
@connection.connection_handler
def remove_record(cursor, table, id_):
    cursor.execute(

        sql.SQL("delete from {table} where {id} = {given_id}").format(
            table=sql.Identifier(table), id=sql.Identifier('id'),
            given_id=sql.Literal(id_))

    )
