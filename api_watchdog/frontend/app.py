import json

from flask import Flask, render_template, request

from api_watchdog import config
from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.config import Config
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData
from api_watchdog.frontend.fake_test_case_histories import api_test_case_histories

app = Flask(__name__)
testing_config_file_path = config.CONFIG_FILE_PATH


def parse_optional_dict_from_string(string: str) -> dict:
    if string.strip() == '' or string.strip() == 'null' or string.strip() == 'None' or string is None:
        return None

    return json.loads(string)


def parse_request_method_from_string(string: str) -> RequestMethod:
    string = string.strip().lower()
    if string == 'get':
        return RequestMethod.GET
    elif string == 'post':
        return RequestMethod.POST
    elif string == 'put':
        return RequestMethod.PUT
    elif string == 'delete':
        return RequestMethod.DELETE
    else:
        raise ValueError(f'Invalid request method: {string}')


def parse_api_test_case_from_request():
    identifier = request.form.get('identifier')
    url = request.form.get('url')
    request_method = parse_request_method_from_string(request.form.get('method'))
    request_body = parse_optional_dict_from_string(request.form.get('request_data'))
    expected_response_status_code = int(request.form.get('status_code'))
    expected_response_body = parse_optional_dict_from_string(request.form.get('expected_response_data'))
    timeout_sec = int(request.form.get('timeout_sec'))

    request_data = RequestData(method=request_method, body=request_body)
    response_data = ResponseData(status_code=expected_response_status_code, body=expected_response_body)
    api_test_case = ApiTestCase(
        identifier=identifier,
        url=url,
        request_data=request_data,
        expected_response_data=response_data,
        timeout_sec=timeout_sec
    )
    return api_test_case


# Define routes for the two subpages
@app.route('/add-test-case')
def add_test_case():
    return render_template('add_test_case.html')


@app.route('/result/<string:test_case_id>')
def result(test_case_id):
    for api_test_case_history in api_test_case_histories:
        if api_test_case_history.test_case.identifier == test_case_id:
            return render_template('result.html', test_case_history=api_test_case_history)


@app.route('/')
def results():
    return render_template('results.html', test_case_histories=api_test_case_histories)


@app.route('/process-new-test-case', methods=['POST'])
def process_new_test_case():
    exception = None
    api_test_case = None

    try:
        if request.method == 'POST':
            api_test_case = parse_api_test_case_from_request()
            testing_config = Config.from_file(testing_config_file_path)
            testing_config.add_api_test_case(api_test_case)
            testing_config.to_file(testing_config_file_path)

    except Exception as e:
        exception = e

    return render_template('process_new_test_case.html', exception=exception, api_test_case=api_test_case)


if __name__ == '__main__':
    app.run(debug=True)
