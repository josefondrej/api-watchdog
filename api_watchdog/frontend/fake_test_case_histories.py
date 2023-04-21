from datetime import datetime

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_record import ApiTestCaseRecord
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData
from api_watchdog.frontend.api_test_case_history import ApiTestCaseHistory

api_test_case_histories = [
    ApiTestCaseHistory(
        test_case=ApiTestCase(
            identifier='test_case_1',
            url='http://localhost:5000/test_case_1',
            request_data=RequestData(method=RequestMethod.GET, body={'foo': 'bar'}),
            expected_response_data=ResponseData(status_code=200, body={'foo': 'bar'})
        ),
        records=[
            ApiTestCaseRecord(
                result=CompressedApiTestCaseResult(
                    api_test_case_identifier='test_case_1',
                    status=ApiTestCaseResultStatus.PASSED
                ),
                timestamp=datetime(2020, 1, 1, 0, 0, 0)
            ),
            ApiTestCaseRecord(
                result=CompressedApiTestCaseResult(
                    api_test_case_identifier='test_case_1',
                    status=ApiTestCaseResultStatus.FAILED,
                    response_data=ResponseData(status_code=500, body={'foo': 'bar'})
                ),
                timestamp=datetime(2021, 1, 1, 0, 0, 1)
            ),
            ApiTestCaseRecord(
                result=CompressedApiTestCaseResult(
                    api_test_case_identifier='test_case_1',
                    status=ApiTestCaseResultStatus.ERROR,
                    exception=Exception('Something went wrong')
                ),
                timestamp=datetime(2022, 1, 1, 0, 0, 2)
            )

        ]
    ),
    ApiTestCaseHistory(
        test_case=ApiTestCase(
            identifier='test_case_2',
            url='http://localhost:5000/test_case_2',
            request_data=RequestData(method=RequestMethod.GET, body={'foo': 'bar'}),
            expected_response_data=ResponseData(status_code=200, body={'foo': 'bar'})
        ),
        records=[
            ApiTestCaseRecord(
                result=CompressedApiTestCaseResult(
                    api_test_case_identifier='test_case_2',
                    status=ApiTestCaseResultStatus.PASSED
                ),
                timestamp=datetime(2020, 1, 1, 0, 0, 0)
            ),
            ApiTestCaseRecord(
                result=CompressedApiTestCaseResult(
                    api_test_case_identifier='test_case_2',
                    status=ApiTestCaseResultStatus.PASSED,
                    response_data=ResponseData(status_code=500, body={'foo': 'bar'})
                ),
                timestamp=datetime(2021, 1, 1, 0, 0, 1)
            ),
            ApiTestCaseRecord(
                result=CompressedApiTestCaseResult(
                    api_test_case_identifier='test_case_2',
                    status=ApiTestCaseResultStatus.PASSED,
                    exception=Exception('Something went wrong')
                ),
                timestamp=datetime(2022, 1, 1, 0, 0, 2)
            )

        ]
    )
]
