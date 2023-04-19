from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_result import ApiTestCaseResult
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData


def test_to_dict():
    api_test_case_result = ApiTestCaseResult(
        api_test_case=ApiTestCase(
            'test-example-com', 'http://example.com', RequestData(RequestMethod.GET), ResponseData(200), timeout_sec=1),
        status=ApiTestCaseResultStatus.PASSED,
        response_data=ResponseData(200)
    )
    assert api_test_case_result.to_dict() == {
        'api_test_case': {
            'identifier': 'test-example-com',
            'url': 'http://example.com',
            'request_data': {'method': 'GET', 'body': {}},
            'expected_response_data': {'status_code': 200, 'body': {}},
            'timeout_sec': 1.0
        },
        'status': 'PASSED',
        'exception': None,
        'response_data': {'status_code': 200, 'body': {}}
    }


def test_from_dict():
    api_test_case_result = ApiTestCaseResult.from_dict({
        'api_test_case': {
            'identifier': 'test-example-com',
            'url': 'http://example.com',
            'request_data': {'method': 'GET', 'body': {}},
            'expected_response_data': {'status_code': 200, 'body': {}},
            'timeout_sec': 1.0
        },
        'status': 'PASSED',
        'exception': None,
        'response_data': {'status_code': 200, 'body': {}}
    })
    assert api_test_case_result.api_test_case.identifier == 'test-example-com'
    assert api_test_case_result.api_test_case.url == 'http://example.com'
    assert api_test_case_result.api_test_case.request_data.method == RequestMethod.GET
    assert api_test_case_result.api_test_case.request_data.body == {}
    assert api_test_case_result.api_test_case.expected_response_data.status_code == 200
    assert api_test_case_result.api_test_case.expected_response_data.body == {}
    assert api_test_case_result.api_test_case.timeout_sec == 1.0
    assert api_test_case_result.status == ApiTestCaseResultStatus.PASSED
    assert api_test_case_result.response_data.status_code == 200
    assert api_test_case_result.response_data.body == {}


def test_compress_passed():
    api_test_case_result = ApiTestCaseResult(
        api_test_case=ApiTestCase(
            'test-example-com', 'http://example.com', RequestData(RequestMethod.GET), ResponseData(200), timeout_sec=1),
        status=ApiTestCaseResultStatus.PASSED,
        response_data=ResponseData(200)
    )
    compressed_api_test_case_result = api_test_case_result.compress()
    assert compressed_api_test_case_result.api_test_case_identifier == 'test-example-com'
    assert compressed_api_test_case_result.status == ApiTestCaseResultStatus.PASSED
    assert compressed_api_test_case_result.exception is None
    assert compressed_api_test_case_result.response_data is None


def test_compress_not_passed():
    api_test_case_result = ApiTestCaseResult(
        api_test_case=ApiTestCase(
            'test-example-com', 'http://example.com', RequestData(RequestMethod.GET), ResponseData(200), timeout_sec=1),
        status=ApiTestCaseResultStatus.FAILED,
        response_data=ResponseData(400),
        exception='Exception'
    )

    compressed_api_test_case_result = api_test_case_result.compress()
    assert compressed_api_test_case_result.api_test_case_identifier == 'test-example-com'
    assert compressed_api_test_case_result.status == ApiTestCaseResultStatus.FAILED
    assert compressed_api_test_case_result.exception == 'Exception'
    assert compressed_api_test_case_result.response_data.status_code == 400
    assert compressed_api_test_case_result.response_data.body == {}
