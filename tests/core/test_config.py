from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.config import Config
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData


def test_to_dict():
    config = Config(
        api_test_cases=[
            ApiTestCase(
                url='http://example.com',
                request_data=RequestData(
                    method=RequestMethod.GET,
                    body={'foo': 'bar'}
                ),
                expected_response_data=ResponseData(
                    status_code=200,
                    body={'foo': 'bar'}
                ),
                timeout_sec=5.0
            )
        ],
        request_frequency_sec=1
    )
    assert config.to_dict() == {
        'api_test_cases': [
            {
                'url': 'http://example.com',
                'request_data': {
                    'method': 'GET',
                    'body': {'foo': 'bar'}
                },
                'expected_response_data': {
                    'status_code': 200,
                    'body': {'foo': 'bar'}
                },
                'timeout_sec': 5.0
            }
        ],
        'request_frequency_sec': 1
    }


def test_from_dict():
    config = Config.from_dict({
        'api_test_cases': [
            {
                'url': 'http://example.com',
                'request_data': {
                    'method': 'GET',
                    'body': {'foo': 'bar'}
                },
                'expected_response_data': {
                    'status_code': 200,
                    'body': {'foo': 'bar'}
                },
                'timeout_sec': 5.0
            }
        ],
        'request_frequency_sec': 1
    })
    assert len(config.api_test_cases) == 1
    assert config.api_test_cases[0].url == 'http://example.com'
    assert config.api_test_cases[0].request_data.method == RequestMethod.GET
    assert config.api_test_cases[0].request_data.body == {'foo': 'bar'}
    assert config.api_test_cases[0].expected_response_data.status_code == 200
    assert config.api_test_cases[0].expected_response_data.body == {'foo': 'bar'}
    assert config.api_test_cases[0].timeout_sec == 5.0
    assert config.request_frequency_sec == 1
