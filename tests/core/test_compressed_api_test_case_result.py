from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult
from api_watchdog.core.response_data import ResponseData


def test_to_dict():
    compressed_api_test_case_result = CompressedApiTestCaseResult(
        api_test_case_identifier='api_test_case_identifier',
        status=ApiTestCaseResultStatus.PASSED,
        response_data=ResponseData(
            status_code=200,
            body={'key': 'value'}
        ),
        exception='exception'
    )
    assert compressed_api_test_case_result.to_dict() == {
        'api_test_case_identifier': 'api_test_case_identifier',
        'status': 'PASSED',
        'response_data': {
            'status_code': 200,
            'body': {'key': 'value'}
        },
        'exception': 'exception'
    }


def test_from_dict():
    compressed_api_test_case_result = CompressedApiTestCaseResult.from_dict({
        'api_test_case_identifier': 'api_test_case_identifier',
        'status': 'PASSED',
        'response_data': {
            'status_code': 200,
            'body': {'key': 'value'}
        },
        'exception': 'exception'
    })
    assert compressed_api_test_case_result.api_test_case_identifier == 'api_test_case_identifier'
    assert compressed_api_test_case_result.status == ApiTestCaseResultStatus.PASSED
    assert compressed_api_test_case_result.response_data == ResponseData(
        status_code=200,
        body={'key': 'value'}
    )
    assert compressed_api_test_case_result.exception == 'exception'
