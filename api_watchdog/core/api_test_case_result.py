from typing import Optional, Dict

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult
from api_watchdog.core.response_data import ResponseData
from api_watchdog.core.serializable import Serializable


class ApiTestCaseResult(Serializable):
    def __init__(self, api_test_case: ApiTestCase, status: ApiTestCaseResultStatus,
                 response_data: Optional[ResponseData] = None,
                 exception: Optional[str] = None):
        self._api_test_case = api_test_case
        self._status = status
        self._response_data = response_data
        self._exception = exception

    @property
    def api_test_case(self) -> ApiTestCase:
        return self._api_test_case

    @property
    def status(self) -> ApiTestCaseResultStatus:
        return self._status

    @property
    def response_data(self) -> Optional[ResponseData]:
        return self._response_data

    @property
    def exception(self) -> Optional[str]:
        return self._exception

    def to_dict(self) -> Dict:
        return {
            'api_test_case': self._api_test_case.to_dict(),
            'status': self._status.value,
            'response_data': self._response_data.to_dict() if self._response_data else None,
            'exception': self._exception
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ApiTestCaseResult':
        return cls(
            api_test_case=ApiTestCase.from_dict(data['api_test_case']),
            status=ApiTestCaseResultStatus(data['status']),
            response_data=ResponseData.from_dict(data['response_data']) if data['response_data'] else None,
            exception=data['exception']
        )

    def compress(self) -> 'CompressedApiTestCaseResult':
        compressed_response_data = None
        if self.status != ApiTestCaseResultStatus.PASSED:
            compressed_response_data = self.response_data

        return CompressedApiTestCaseResult(
            api_test_case_identifier=self.api_test_case.identifier,
            status=self.status,
            response_data=compressed_response_data,
            exception=self.exception
        )
