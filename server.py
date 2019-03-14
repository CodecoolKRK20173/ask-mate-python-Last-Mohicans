from flask import Flask, render_template, redirect, request, url_for
import data_manager
import util
import connection
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = connection.UPLOAD_FOLDER


@app.route('/')
def index():
    return redirect('/list')


@app.route('/list')
def questions_list():
    regular_questions = data_manager.get_questions()
    regular_questions = {int(key): value for key, value in regular_questions.items()}
    ordered_questions = util.reversed_order_dict(regular_questions)
    return render_template('list.html', questions=ordered_questions)


@app.route('/question/<question_id>')
# @app.route('/question/<question_id>/edit')
# @app.route('/question/<question_id>/delete')
def route_question(question_id=None):
    if question_id:
        data_manager.update_question_view_number(question_id)
        questions = data_manager.get_questions()
        regular_answers = data_manager.get_answers_by_question_id(question_id)
        regular_answers = {int(key): value for key, value in regular_answers.items()}
        ordered_answers = util.reversed_order_dict(regular_answers)
        return render_template('question.html', question=questions[question_id], answers=ordered_answers, question_id=question_id)
    return redirect('/list')

# @app.route('/question/<question_id>/<option>') # zamiast 5 innych
# options = ['edit', 'delete', 'new-answer', 'vote-up', 'vote-down']


@app.route('/question/<question_id>/vote-up', methods=['POST'])
def question_vote_up(question_id):
    data_manager.update_question_vote_number(question_id, 1)
    return redirect('/list')


@app.route('/question/<question_id>/vote-down', methods=['POST'])
def question_vote_down(question_id):
    data_manager.update_question_vote_number(question_id, -1)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote-up', methods=['POST'])
def answer_vote_up(answer_id):
    question_id = data_manager.update_answer_vote_number(answer_id, 1)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/vote-down', methods=['POST'])
def answer_vote_down(answer_id):
    question_id = data_manager.update_answer_vote_number(answer_id, -1)
    return redirect(f'/question/{question_id}')


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':

        values = [data_manager.get_new_question_id(),
                  util.get_timestamp(),
                  '0',
                  '0',
                  request.form['title'],
                  request.form['message'],
                  '']

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = url_for('static', filename=filename)

            # return render_template('list.html', questions=ordered_questions, filename=filename)

            values[6] = url

        data_manager.add_question(values)

        return redirect('/')

    else:
        question_headers = data_manager.get_question_fields()[4:7]
        return render_template('add-question.html', question_headers=question_headers)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_add_answer(question_id):
    # question_id = question_id
    if request.method == 'GET':
        questions = data_manager.get_questions()
        answers = data_manager.get_answers_by_question_id(question_id)
        return render_template('answer.html', question=questions[question_id], answers=answers, question_id=question_id)

    elif request.method == 'POST':

        values = [data_manager.get_new_answer_id(),
                  util.get_timestamp(),
                  '0',
                  question_id,
                  request.form['message'],
                  '']

        data_manager.add_answer(values)

        return redirect(f'/question/{question_id}')


@app.route('/question/<question_id>/delete', methods=['POST'])
def route_remove_question(question_id):
    data_manager.remove_question(question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def route_remove_answer(answer_id):
    question_id = data_manager.remove_answer(answer_id)
    return redirect(f'/question/{question_id}')


# @app.route('/question/<question_id>/add-image', methods=['POST'])
# def question_add_image(question_id):
#     data_manager.update_question_vote_number(question_id, -1)
#
#     return redirect('/list')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in connection.ALLOWED_EXTENSIONS


@app.route('/list', methods=['GET', 'POST'])
def upload_file():
    regular_questions = data_manager.get_questions()
    regular_questions = {int(key): value for key, value in regular_questions.items()}
    ordered_questions = util.reversed_order_dict(regular_questions)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = url_for('static', filename=filename)

            return render_template('list.html', questions=ordered_questions, filename=filename)
    return render_template('list.html', questions=ordered_questions) #, filename=filename)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
            )
