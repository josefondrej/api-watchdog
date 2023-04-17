from json import JSONDecodeError
from typing import Callable

import requests

from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData


def _method_to_function(method: RequestMethod) -> Callable:
    return getattr(requests, str(method.value).lower())


def make_request(url: str, request_data: RequestData, timeout_sec: float) -> ResponseData:
    method = _method_to_function(request_data.method)
    response = method(url=url, timeout=timeout_sec, json=request_data.body)
    try:
        json = response.json()
    except JSONDecodeError:
        json = None

    return ResponseData(status_code=response.status_code, body=json)
