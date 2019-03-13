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
#@app.route('/question/<question_id>/edit')
#@app.route('/question/<question_id>/delete')
#@app.route('/question/<question_id>/new-answer')
#@app.route('/question/<question_id>/vote-up')
#@app.route('/question/<question_id>/vote-down')
def route_question(question_id=None):
    questions = data_manager.get_questions()
    if question_id:
        answers = data_manager.get_answers_by_question_id(question_id)
        return render_template('question.html', question=questions[question_id], answers=answers)
    return redirect('/list')

# @app.route('/question/<question_id>/<option>') # zamiast 5 innych
# options = ['edit', 'delete', 'new-answer', 'vote-up', 'vote-down']


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    question_headers = connection.QUESTION_FIELDS[4:]
    if request.method == 'POST':
        values = []
        for header in question_headers:
            values.append(request.form[header])

        added_question = dict(zip(question_headers, values))
        connection.export_data(added_question, connection.QUESTION_FILE)

        return redirect('/')

    else:

        return render_template('add-question.html', question_headers=question_headers)


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
