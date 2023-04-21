from typing import Dict

from api_watchdog.core.request_data import RequestData
from api_watchdog.core.response_data import ResponseData
from api_watchdog.core.serializable import Serializable


class ApiTestCase(Serializable):
    def __init__(self, identifier: str, url: str, request_data: RequestData, expected_response_data: ResponseData,
                 timeout_sec: float = 5.0):
        self._identifier = identifier
        self._url = url
        self._request_data = request_data
        self._expected_response_data = expected_response_data
        self._timeout_sec = float(timeout_sec)

    def __str__(self):
        return f'ApiTestCase(identifier={self._identifier}, url={self._url})'

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def url(self) -> str:
        return self._url

    @property
    def request_data(self) -> RequestData:
        return self._request_data

    @property
    def expected_response_data(self) -> ResponseData:
        return self._expected_response_data

    @property
    def timeout_sec(self) -> float:
        return self._timeout_sec

    def to_dict(self) -> Dict:
        return {
            'identifier': self._identifier,
            'url': self._url,
            'request_data': self._request_data.to_dict(),
            'expected_response_data': self._expected_response_data.to_dict(),
            'timeout_sec': self._timeout_sec
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ApiTestCase':
        return cls(
            identifier=data['identifier'],
            url=data['url'],
            request_data=RequestData.from_dict(data['request_data']),
            expected_response_data=ResponseData.from_dict(data['expected_response_data']),
            timeout_sec=data['timeout_sec']
        )
