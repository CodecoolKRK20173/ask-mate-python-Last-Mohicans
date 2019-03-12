from flask import Flask, render_template, redirect, request
import data_manager
import util

app = Flask(__name__)


@app.route('/list')
def route_list():
    pass


@app.route('/question')
@app.route('/question/<question_id>')
@app.route('/question/<question_id>/edit')
@app.route('/question/<question_id>/delete')
@app.route('/question/<question_id>/new-answer')
@app.route('/question/<question_id>/vote-up')
@app.route('/question/<question_id>/vote-down')
def route_question():
    pass
# @app.route('/question/<question_id>/<option>') # zamiast 5 innych
# options = ['edit', 'delete', 'new-answer', 'vote-up', 'vote-down']


@app.route('/add-question')
def route_list():
    pass


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,  # Allow verbose error reports
        port=8000  # Set custom port
    )