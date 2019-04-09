from flask import Flask, flash, render_template, redirect, request, url_for
import data_manager
import util
import connection
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = connection.UPLOAD_FOLDER
app.secret_key = 'camel toe'


def allowed_file(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in connection.ALLOWED_EXTENSIONS)


@app.route('/')
def index():
    questions = data_manager.get_latest_questions()
    return render_template('list.html', questions=questions, latest=True)


@app.route('/list')
def questions_list():
    questions = data_manager.get_questions()
    return render_template('list.html', questions=questions, latest=False)


@app.route('/list/<option>')
def questions_list_sorted(option):
    questions = data_manager.get_questions(option)
    return render_template('list.html', questions=questions, latest=False)


@app.route('/question/<question_id>')
def route_question(question_id):
    data_manager.update_question_view_number(question_id)
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comments()
    questions_comments_ids = [comment['question_id'] for comment in comments if comment['question_id']]
    answer_comments_ids = [comment['answer_id'] for comment in comments if comment['answer_id']]
    return render_template('question.html', question=question, answers=answers, comments=comments,
                           qc_ids=questions_comments_ids, qa_ids=answer_comments_ids)


@app.route('/search')
def route_question_search():
    search_phrase = request.args.get('q')
    search_phrase = '%' + search_phrase + '%'
    questions = data_manager.get_questions_by_phrase(search_phrase)

    return render_template('list.html', questions=questions)
    # return render_template('question.html', question=questions)
    # return redirect(f'/question/{question_id}')

    # data_manager.update_question_view_number(question_id)
    # question = data_manager.get_question_by_id(question_id)
    # answers = data_manager.get_answers_by_question_id(question_id)
    # return render_template('question.html', question=question, answers=answers)


@app.route('/question/<question_id>/<vote>', methods=['POST'])
def question_vote(question_id, vote):
    value = 0
    if vote == 'vote-up':
        value = 1
    elif vote == 'vote-down':
        value = -1
    data_manager.update_vote_number('question', question_id, value)
    return redirect('/list')


@app.route('/answer/<answer_id>/<vote>', methods=['POST'])
def answer_vote(answer_id, vote):
    value = 0
    if vote == 'vote-up':
        value = 1
    elif vote == 'vote-down':
        value = -1
    data_manager.update_vote_number('answer', answer_id, value)
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():

    if request.method == 'POST':
        filename = ''
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        values = [util.get_timestamp(),
                  '0',
                  '0',
                  request.form['title'],
                  request.form['message'],
                  filename]

        data_manager.add_question(values)
        return redirect('/')

    else:
        return render_template('add-question.html', id=None, question=None)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_question(question_id):
    if request.method == 'POST':
        image = ''

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename

        values = [question_id,
                  request.form['title'],
                  request.form['message'],
                  image]

        data_manager.update_question(values)
        return redirect('/')
    else:
        question = data_manager.get_question_by_id(question_id)
        return render_template('add-question.html', id=question_id, question=question)


@app.route('/question/<question_id>/delete', methods=['POST'])
def route_remove_question(question_id):
    data_manager.remove_record('question', question_id)
    return redirect('/list')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_add_answer(question_id):
    if request.method == 'GET':
        question = data_manager.get_question_by_id(question_id)
        answers = data_manager.get_answers_by_question_id(question_id)
        return render_template('answer.html', question=question, answers=answers)

    elif request.method == 'POST':
        filename = ''

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        values = [util.get_timestamp(),
                  '0',
                  question_id,
                  request.form['message'],
                  filename]

        data_manager.add_answer(values)

        return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    answer = data_manager.get_answer_by_id(answer_id)
    if request.method == 'POST':
        image = ''

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename

        values = [answer_id,
                  request.form['message'],
                  image]

        data_manager.update_answer(values)
        return redirect(f'/question/{question_id}')
    else:
        question = data_manager.get_question_by_id(question_id)
        return render_template('answer.html', id=answer_id, question=question, answer=answer)


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def route_remove_answer(answer_id):
    question_id = data_manager.get_question_id_by_answer_id(answer_id)
    data_manager.remove_record('answer', answer_id)
    return redirect(f'/question/{question_id}')


@app.route('/comment/<what>/<id_>/new-comment', methods=['GET', 'POST'])
def route_add_comment(what, id_):
    if request.method == 'GET':
        question = None
        answer = None
        if what == 'question':
            question = data_manager.get_question_by_id(id_)
        elif what == 'answer':
            answer = data_manager.get_answer_by_id(id_)
        return render_template('comment.html', question=question, answer=answer, comment=None)
    elif request.method == 'POST':
        answer_id = None
        question_id = None
        if what == 'question':
            question_id = id_
        elif what == 'answer':
            answer_id = id_

        values = [question_id,
                  answer_id,
                  request.form['message'],
                  util.get_timestamp(),
                  '0']

        data_manager.add_comment(values)

        if answer_id:
            question_id = data_manager.get_question_id_by_answer_id(answer_id)

        return redirect(f'/question/{question_id}')


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def route_edit_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    if request.method == 'GET':
        question=None
        answer=None
        if comment['question_id']:
            question = data_manager.get_question_by_id(comment['question_id'])
        else:
            answer = data_manager.get_answer_by_id(comment['answer_id'])
        return render_template('comment.html', question=question, answer=answer, comment=comment)
    elif request.method == 'POST':

        values = [comment_id, request.form['message'], comment['edited_count']+1]
        data_manager.update_comment(values)

        if comment['question_id']:
            question_id = comment['question_id']
        else:
            answer = data_manager.get_answer_by_id(comment['answer_id'])
            question_id = answer['question_id']

        return redirect(f'/question/{question_id}')


@app.route('/comment/<comment_id>/delete', methods=['POST'])
def route_remove_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    if comment['question_id']:
        question_id = comment['question_id']
    else:
        answer = data_manager.get_answer_by_id(comment['answer_id'])
        question_id = answer['question_id']
    data_manager.remove_record('comment', comment_id)
    return redirect(f'/question/{question_id}')


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
            )
