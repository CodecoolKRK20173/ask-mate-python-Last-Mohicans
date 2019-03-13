from flask import Flask, render_template, redirect, request
import data_manager
import util

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/list')


@app.route('/list')
def list():
    questions = data_manager.get_questions()
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
# @app.route('/question/<question_id>/edit')
# @app.route('/question/<question_id>/delete')
# @app.route('/question/<question_id>/new-answer')
# @app.route('/question/<question_id>/vote-up')
# @app.route('/question/<question_id>/vote-down')
def route_question(question_id=None):
    if question_id:
        questions = data_manager.update_question_view_number(question_id)
        answers = data_manager.get_answers_by_question_id(question_id)
        return render_template('question.html', question=questions[question_id], answers=answers)
    return redirect('/list')

# @app.route('/question/<question_id>/<option>') # zamiast 5 innych
# options = ['edit', 'delete', 'new-answer', 'vote-up', 'vote-down']


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        values = []
        question_headers = data_manager.get_question_fields()[1:]

        id = data_manager.get_new_question_id()  # ID
        values.append(util.get_timestamp())  # SUBMISSION_TIME
        values.append('0')  # VIEW_NUMBER
        values.append('0')  # VOTE_NUMBER
        values.append(request.form['title'])  # TITLE
        values.append(request.form['message'])  # MESSAGE
        values.append('')  # IMAGE

        added_question = dict(zip(question_headers, values))
        print(added_question)
        data_manager.add_question(id, added_question)

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
