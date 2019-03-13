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
# @app.route('/question/<question_id>/edit')
# @app.route('/question/<question_id>/delete')
# @app.route('/question/<question_id>/new-answer')
def route_question(question_id=None):
    if question_id:
        data_manager.update_question_view_number(question_id)
        questions = data_manager.get_questions()
        answers = data_manager.get_answers_by_question_id(question_id)
        return render_template('question.html', question=questions[question_id], answers=answers)
    return redirect('/list')

# @app.route('/question/<question_id>/<option>') # zamiast 5 innych
# options = ['edit', 'delete', 'new-answer', 'vote-up', 'vote-down']


@app.route('/question/<question_id>/vote-up', methods=['POST'])
def question_vote_up(question_id=None):
    data_manager.update_question_vote_number(question_id, 1)
    return redirect('/list')


@app.route('/question/<question_id>/vote-down', methods=['POST'])
def question_vvote_down(question_id=None):
    data_manager.update_question_vote_number(question_id, -1)
    return redirect('/list')


@app.route('/answer/<answer_id>/vote-up', methods=['POST'])
def answer_vote_up(answer_id=None):
    question_id = data_manager.update_answer_vote_number(answer_id, 1)
    return redirect(f'/question/{question_id}')


@app.route('/answer/<answer_id>/vote-down', methods=['POST'])
def answer_vote_down(answer_id=None):
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
        question_headers = data_manager.get_question_fields()[4:6]
        return render_template('add-question.html', question_headers=question_headers)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
