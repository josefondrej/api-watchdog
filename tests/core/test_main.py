from unittest.mock import patch

import pytest

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.main import run_api_test_case
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData


def mock_make_request_expected_response(url, request_data, timeout_sec):
    return ResponseData(status_code=200, body={'foo': 'bar'})


def mock_make_request_unexpected_response(url, request_data, timeout_sec):
    return ResponseData(status_code=200, body={'foo': 'baz'})


def mock_make_request_error(url, request_data, timeout_sec):
    raise Exception('Some error')


@pytest.fixture
def api_test_case():
    return ApiTestCase(
        identifier='test-example-com',
        url='http://example.com',
        request_data=RequestData(RequestMethod.GET),
        expected_response_data=ResponseData(200, {'foo': 'bar'}),
        timeout_sec=1
    )


def test_run_api_test_case_expected_response(api_test_case):
    with patch('api_watchdog.core.main.make_request', mock_make_request_expected_response):
        api_test_case_record = run_api_test_case(api_test_case)

    assert api_test_case_record.result.status == ApiTestCaseResultStatus.PASSED
    assert api_test_case_record.result.response_data is None
    assert api_test_case_record.result.exception is None


def test_run_api_test_case_unexpected_response(api_test_case):
    with patch('api_watchdog.core.main.make_request', mock_make_request_unexpected_response):
        api_test_case_record = run_api_test_case(api_test_case)

    assert api_test_case_record.result.status == ApiTestCaseResultStatus.FAILED
    assert api_test_case_record.result.response_data.body == {'foo': 'baz'}
    assert api_test_case_record.result.exception is None


def test_run_api_test_case_error(api_test_case):
    with patch('api_watchdog.core.main.make_request', mock_make_request_error):
        api_test_case_record = run_api_test_case(api_test_case)

    assert api_test_case_record.result.status == ApiTestCaseResultStatus.ERROR
    assert api_test_case_record.result.response_data is None
    assert api_test_case_record.result.exception == 'Some error'
