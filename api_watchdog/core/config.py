from typing import List, Optional, Dict

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.serializable import Serializable


class Config(Serializable):
    def __init__(self, api_test_cases: Optional[List[ApiTestCase]] = None):
        self._api_test_cases = api_test_cases or []

    @property
    def api_test_cases(self) -> List[ApiTestCase]:
        return self._api_test_cases

    def add_api_test_case(self, api_test_case: ApiTestCase):
        self._api_test_cases.append(api_test_case)

    def to_dict(self) -> Dict:
        return {
            'api_test_cases': [api_test_case.to_dict() for api_test_case in self._api_test_cases]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Config':
        return cls(api_test_cases=[ApiTestCase.from_dict(api_test_case) for api_test_case in data['api_test_cases']])
