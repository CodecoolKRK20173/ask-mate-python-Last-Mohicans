from flask import Flask, render_template, redirect, request
import data_manager
import util

app = Flask(__name__)


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
    questions = data_manager.get_questions()
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template('question.html', question=questions[question_id], answers=answers, question_id=question_id)

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
        data_manager.add_question(values)
        return redirect('/')
    else:
        return render_template('add-question.html', id=None, question=None)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_question(question_id):
    if request.method == 'POST':
        question = data_manager.get_question_by_id(question_id)
        question['title'] = request.form['title']
        question['message'] = request.form['message']
        data_manager.update_question(question, question_id)
        return redirect('/')
    else:
        question = data_manager.get_question_by_id(question_id)
        return render_template('add-question.html', id=question_id, question=question)


@app.route('/question/<question_id>/delete', methods=['POST'])
def route_remove_question(question_id):
    data_manager.remove_question(question_id)
    return redirect('/list')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_add_answer(question_id):
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

        return redirect('/question/'+question_id)


@app.route('/answer/<answer_id>/delete', methods=['POST'])
def route_remove_answer(answer_id):
    question_id = data_manager.remove_answer(answer_id)
    return redirect(f'/question/{question_id}')


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
