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
    return redirect('/list')


@app.route('/list')
def questions_list():
    questions = data_manager.get_questions()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def route_question(question_id):
    data_manager.update_question_view_number(question_id)
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    comments = data_manager.get_comments()
    return render_template('question.html', question=question, answers=answers, comments=comments)


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

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
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
        question = data_manager.get_question_by_id(question_id)
        # question['title'] = request.form['title']
        # question['message'] = request.form['message']
        image = ''

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            image = filename

        values = [question_id,
                  request.form['title'],
                  request.form['message'],
                  image]

        # data_manager.add_question(values)

        data_manager.update_question(values)  #question_id, question,
        return redirect('/')
    else:

        # question_headers = data_manager.get_question_fields()[4:7]
        # return render_template('add-question.html', question_headers=question_headers)

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

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
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

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
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


# @app.route('/question/<question_id>/add-image', methods=['POST'])
# def question_add_image(question_id):
#     data_manager.update_question_vote_number(question_id, -1)
#
#     return redirect('/list')


# @app.route('/list', methods=['GET', 'POST'])
# def upload_file():
#     regular_questions = data_manager.get_questions()
#     regular_questions = {int(key): value for key, value in regular_questions.items()}
#     ordered_questions = util.reversed_order_dict(regular_questions)
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit a empty part without filename
#         if file.filename == '':
#             # flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             url = url_for('static', filename=filename)
#
#             return render_template('list.html', questions=ordered_questions, filename=filename)
#     return render_template('list.html', questions=ordered_questions) #, filename=filename)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
            )
