from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData


def test_to_dict():
    api_test_case = ApiTestCase('test-example-com', 'http://example.com', RequestData(RequestMethod.GET),
                                ResponseData(200), timeout_sec=1)
    assert api_test_case.to_dict() == {
        'identifier': 'test-example-com',
        'url': 'http://example.com',
        'request_data': {'method': 'GET', 'body': {}},
        'expected_response_data': {'status_code': 200, 'body': {}},
        'timeout_sec': 1.0
    }


def test_from_dict():
    api_test_case = ApiTestCase.from_dict({
        'identifier': 'test-example-com',
        'url': 'http://example.com',
        'request_data': {'method': 'GET', 'body': {}},
        'expected_response_data': {'status_code': 200, 'body': {}},
        'timeout_sec': 1.0
    })
    assert api_test_case.identifier == 'test-example-com'
    assert api_test_case.url == 'http://example.com'
    assert api_test_case.request_data.method == RequestMethod.GET
    assert api_test_case.request_data.body == {}
    assert api_test_case.expected_response_data.status_code == 200
    assert api_test_case.expected_response_data.body == {}
    assert api_test_case.timeout_sec == 1.0
