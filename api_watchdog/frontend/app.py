from flask import Flask, render_template

from api_watchdog.frontend.fake_test_case_histories import api_test_case_histories

app = Flask(__name__)


# Define routes for the two subpages
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result/<string:test_case_id>')
def result(test_case_id):
    for api_test_case_history in api_test_case_histories:
        if api_test_case_history.test_case.identifier == test_case_id:
            return render_template('result.html', test_case_history=api_test_case_history)


@app.route('/results')
def results():
    return render_template('results.html', test_case_histories=api_test_case_histories)


if __name__ == '__main__':
    app.run(debug=True)
