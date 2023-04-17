from typing import Optional, Dict

from api_watchdog.core.serializable import Serializable


class ResponseData(Serializable):
    def __init__(self, status_code: int, body: Optional[Dict] = None):
        self._status_code = status_code
        self._body = body or {}

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def body(self) -> Dict:
        return self._body

    def to_dict(self) -> Dict:
        return {
            'status_code': self._status_code,
            'body': self._body
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ResponseData':
        return cls(status_code=data['status_code'], body=data['body'])

    def __hash__(self):
        return hash((self.status_code, tuple(sorted(self.body.items()))))

    def __eq__(self, other):
        if not isinstance(other, ResponseData):
            return False
        return self.status_code == other.status_code and self.body == other.body
