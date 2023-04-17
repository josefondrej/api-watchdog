from typing import Optional, Dict

from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.serializable import Serializable


class RequestData(Serializable):
    def __init__(self, method: RequestMethod, body: Optional[Dict] = None):
        self._method = method
        self._body = body or {}

    @property
    def method(self) -> RequestMethod:
        return self._method

    @property
    def body(self) -> Dict:
        return self._body

    def to_dict(self) -> Dict:
        return {
            'method': self._method.value,
            'body': self._body
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'RequestData':
        return cls(method=RequestMethod(data['method']), body=data['body'])
