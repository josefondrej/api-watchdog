from typing import List, Optional, Dict

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.serializable import Serializable
from api_watchdog.core.utils import write_json_atomic, read_json_atomic


class Config(Serializable):
    def __init__(self, api_test_cases: Optional[List[ApiTestCase]] = None, request_frequency_sec: int = 60):
        self._api_test_cases = api_test_cases or []
        self._request_frequency_sec = int(request_frequency_sec)

    @property
    def api_test_cases(self) -> List[ApiTestCase]:
        return self._api_test_cases

    @property
    def request_frequency_sec(self) -> int:
        return self._request_frequency_sec

    def add_api_test_case(self, api_test_case: ApiTestCase):
        self._api_test_cases.append(api_test_case)

    def to_dict(self) -> Dict:
        return {
            'api_test_cases': [api_test_case.to_dict() for api_test_case in self._api_test_cases],
            'request_frequency_sec': self._request_frequency_sec
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Config':
        return cls(
            api_test_cases=[ApiTestCase.from_dict(api_test_case_data) for api_test_case_data in data['api_test_cases']],
            request_frequency_sec=data['request_frequency_sec']
        )

    def to_file(self, file_path: str):
        write_json_atomic(data=self.to_dict(), file_path=file_path)

    @classmethod
    def from_file(cls, file_path: str) -> 'Config':
        return cls.from_dict(data=read_json_atomic(file_path=file_path))
