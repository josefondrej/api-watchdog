from unittest.mock import patch

from api_watchdog.backend.requests_backend import make_request
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod


def test_make_request():
    with patch('api_watchdog.backend.requests_backend.requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'foo': 'bar'}

        response_data = make_request(
            url='http://example.com',
            request_data=RequestData(RequestMethod.GET),
            timeout_sec=1
        )

    assert response_data.status_code == 200
    assert response_data.body == {'foo': 'bar'}
