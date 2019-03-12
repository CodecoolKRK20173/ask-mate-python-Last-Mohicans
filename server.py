from flask import Flask, render_template, redirect, request
import connection

app = Flask(__name__)

@app.route('/')
def index():
    questions = connection.import_data(connection.QUESTION_FILE)
    return render_template('list.html', questions=questions)


if __name__ == '__main__':
    app.run()
