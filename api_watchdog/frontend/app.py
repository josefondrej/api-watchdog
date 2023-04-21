import json
import logging
from typing import List

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from waitress import serve

from api_watchdog import config
from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.config import Config
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData
from api_watchdog.database.db_base import DbBase
from api_watchdog.database.sqlite_db import SqliteDb
from api_watchdog.frontend.api_test_case_history import ApiTestCaseHistory

app = Flask(__name__)
testing_config_file_path = config.CONFIG_FILE_PATH

db_connection_string = config.DATABASE_CONNECTION_STRING
engine = create_engine(db_connection_string)
database = SqliteDb(engine)


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


def validate_identifier(identifier: str):
    #     can only contain _,-,a-z,A-Z,0-9
    #     must start with a-z,A-Z
    #     must be at least 3 characters long
    #     must be at most 100 characters long
    if len(identifier) < 3:
        raise ValueError('Identifier must be at least 3 characters long')
    if len(identifier) > 100:
        raise ValueError('Identifier must be at most 100 characters long')
    if not identifier[0].isalpha():
        raise ValueError('Identifier must start with a letter')
    for char in identifier:
        if not char.isalnum() and char not in ['_', '-']:
            raise ValueError('Identifier can only contain letters, numbers, and _,-')


def parse_api_test_case_from_request():
    identifier = request.form.get('identifier')
    validate_identifier(identifier)
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


def load_api_test_case_history(api_test_case: ApiTestCase, database: DbBase) -> List[ApiTestCaseHistory]:
    records = database.list_api_test_case_records(api_test_case_identifier=api_test_case.identifier)
    api_test_case_history = ApiTestCaseHistory(test_case=api_test_case, records=records)
    return api_test_case_history


# Define routes for the two subpages
@app.route('/add-test-case')
def add_test_case():
    return render_template('add_test_case.html')


@app.route('/result/<string:test_case_id>')
def result(test_case_id):
    testing_config = Config.from_file(testing_config_file_path)
    api_test_case = testing_config.get_test_case(identifier=test_case_id)
    api_test_case_history = load_api_test_case_history(api_test_case=api_test_case, database=database)
    return render_template('result.html', test_case_history=api_test_case_history)


@app.route('/')
def results():
    testing_config = Config.from_file(testing_config_file_path)
    api_test_case_histories = [load_api_test_case_history(api_test_case, database=database)
                               for api_test_case in testing_config.api_test_cases]
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
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    HOST = '0.0.0.0'
    PORT = 5000

    serve(app, host=HOST, port=PORT)
