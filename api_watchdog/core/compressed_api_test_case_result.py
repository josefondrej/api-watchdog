from typing import Optional

from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.response_data import ResponseData
from api_watchdog.core.serializable import Serializable


class CompressedApiTestCaseResult(Serializable):
    def __init__(self, api_test_case_identifier: str, status: ApiTestCaseResultStatus,
                 response_data: Optional[ResponseData] = None,
                 exception: Optional[str] = None):
        self._api_test_case_identifier = api_test_case_identifier
        self._status = status
        self._response_data = response_data
        self._exception = exception

    @property
    def api_test_case_identifier(self) -> str:
        return self._api_test_case_identifier

    @property
    def status(self) -> ApiTestCaseResultStatus:
        return self._status

    @property
    def response_data(self) -> Optional[ResponseData]:
        return self._response_data

    @property
    def exception(self) -> Optional[str]:
        return self._exception

    def to_dict(self) -> dict:
        return {
            'api_test_case_identifier': self._api_test_case_identifier,
            'status': self._status.value,
            'response_data': self._response_data.to_dict() if self._response_data else None,
            'exception': self._exception
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CompressedApiTestCaseResult':
        return cls(
            api_test_case_identifier=data['api_test_case_identifier'],
            status=ApiTestCaseResultStatus(data['status']),
            response_data=ResponseData.from_dict(data['response_data']) if data['response_data'] else None,
            exception=data['exception']
        )
