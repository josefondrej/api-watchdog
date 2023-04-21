from datetime import datetime
from typing import Dict

from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult
from api_watchdog.core.serializable import Serializable


class ApiTestCaseRecord(Serializable):
    def __init__(self, result: CompressedApiTestCaseResult, timestamp: datetime):
        self._result = result
        self._timestamp = timestamp

    @property
    def result(self):
        return self._result

    @property
    def timestamp(self):
        return self._timestamp

    def to_dict(self) -> Dict:
        return {
            'result': self._result.to_dict(),
            'timestamp': self._timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ApiTestCaseRecord':
        return cls(
            result=CompressedApiTestCaseResult.from_dict(data['result']),
            timestamp=datetime.fromisoformat(data['timestamp'])
        )
