from typing import List

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_result import ApiTestCaseResult
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult


def decompress(compressed_api_test_case_result: CompressedApiTestCaseResult,
               api_test_cases: List[ApiTestCase]) -> ApiTestCaseResult:
    api_test_case = next(api_test_case for api_test_case in api_test_cases if
                         api_test_case.identifier == compressed_api_test_case_result.api_test_case_identifier)
    response_data = compressed_api_test_case_result.response_data
    if compressed_api_test_case_result.status == ApiTestCaseResultStatus.PASSED:
        response_data = api_test_case.expected_response_data
    return ApiTestCaseResult(
        api_test_case=api_test_case,
        status=compressed_api_test_case_result.status,
        response_data=response_data,
        exception=compressed_api_test_case_result.exception
    )
