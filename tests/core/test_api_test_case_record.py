from datetime import datetime

from api_watchdog.core.api_test_case_record import ApiTestCaseRecord
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult


def test_to_dict():
    api_test_case_record = ApiTestCaseRecord(
        result=CompressedApiTestCaseResult(
            api_test_case_identifier='test_api_test_case_identifier',
            status=ApiTestCaseResultStatus.PASSED,
            response_data=None,
            exception=None
        ),
        timestamp=datetime.fromisoformat('2021-01-01T00:00:00')
    )

    assert api_test_case_record.to_dict() == {
        'result': {
            'api_test_case_identifier': 'test_api_test_case_identifier',
            'status': 'PASSED',
            'response_data': None,
            'exception': None
        },
        'timestamp': '2021-01-01T00:00:00'
    }


def test_from_dict():
    api_test_case_record = ApiTestCaseRecord.from_dict({
        'result': {
            'api_test_case_identifier': 'test_api_test_case_identifier',
            'status': 'PASSED',
            'response_data': None,
            'exception': None
        },
        'timestamp': '2021-01-01T00:00:00'
    })

    assert api_test_case_record.result.api_test_case_identifier == 'test_api_test_case_identifier'
    assert api_test_case_record.result.status == ApiTestCaseResultStatus.PASSED
    assert api_test_case_record.result.response_data is None
    assert api_test_case_record.result.exception is None
    assert api_test_case_record.timestamp == datetime.fromisoformat('2021-01-01T00:00:00')
