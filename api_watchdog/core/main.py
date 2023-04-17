import logging

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_result import ApiTestCaseResult
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.http_request_backends.requests_backend import make_request

logger = logging.getLogger(__name__)


def run_api_test_case(api_test_case: ApiTestCase) -> ApiTestCaseResult:
    try:
        response_data = make_request(
            url=api_test_case.url,
            request_data=api_test_case.request_data,
            timeout_sec=api_test_case.timeout_sec
        )

        if response_data != api_test_case.expected_response_data:
            return ApiTestCaseResult(
                api_test_case=api_test_case,
                status=ApiTestCaseResultStatus.FAILED,
                response_data=response_data
            )
        else:
            return ApiTestCaseResult(
                api_test_case=api_test_case,
                status=ApiTestCaseResultStatus.PASSED,
                response_data=response_data
            )

    except Exception as exception:
        logger.exception(exception)

        return ApiTestCaseResult(
            api_test_case=api_test_case,
            status=ApiTestCaseResultStatus.ERROR,
            exception=str(exception)
        )
