from typing import List

import pytest

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult
from api_watchdog.core.decompress_api_test_case_result import decompress
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData


@pytest.fixture
def api_test_cases() -> List[ApiTestCase]:
    return [
        ApiTestCase(
            identifier='api_test_case_identifier',
            url='http://example.com',
            request_data=RequestData(RequestMethod.GET, {'key': 'value_request'}),
            expected_response_data=ResponseData(200, {'key': 'value_response'})
        ),
        ApiTestCase(
            identifier='api_test_case_identifier_2',
            url='http://example2.com',
            request_data=RequestData(RequestMethod.GET, {'key': 'value_request2'}),
            expected_response_data=ResponseData(200, {'key': 'value_response2'})
        )
    ]


def test_decompress_passed(api_test_cases):
    compressed_api_test_case_result = CompressedApiTestCaseResult(
        api_test_case_identifier='api_test_case_identifier',
        status=ApiTestCaseResultStatus.PASSED
    )

    api_test_case_result = decompress(compressed_api_test_case_result, api_test_cases)
    assert api_test_case_result.api_test_case.identifier == 'api_test_case_identifier'
    assert api_test_case_result.status == ApiTestCaseResultStatus.PASSED
    assert api_test_case_result.response_data == ResponseData(200, {'key': 'value_response'})
    assert api_test_case_result.exception is None


def test_decompress_failed(api_test_cases):
    compressed_api_test_case_result = CompressedApiTestCaseResult(
        api_test_case_identifier='api_test_case_identifier_2',
        status=ApiTestCaseResultStatus.FAILED,
        response_data=ResponseData(500, {'key': 'value_response'}),
        exception='exception'
    )

    api_test_case_result = decompress(compressed_api_test_case_result, api_test_cases)
    assert api_test_case_result.api_test_case.identifier == 'api_test_case_identifier_2'
    assert api_test_case_result.api_test_case.expected_response_data == ResponseData(200, {'key': 'value_response2'})
    assert api_test_case_result.status == ApiTestCaseResultStatus.FAILED
    assert api_test_case_result.response_data == ResponseData(500, {'key': 'value_response'})
    assert api_test_case_result.exception == 'exception'
