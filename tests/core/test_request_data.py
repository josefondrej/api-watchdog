from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod


def test_to_dict():
    request_data = RequestData(RequestMethod.GET)
    assert request_data.to_dict() == {'method': 'GET', 'body': {}}


def test_to_dict_with_body():
    request_data = RequestData(RequestMethod.GET, {'foo': 'bar'})
    assert request_data.to_dict() == {'method': 'GET', 'body': {'foo': 'bar'}}


def test_from_dict():
    request_data = RequestData.from_dict({'method': 'GET', 'body': {}})
    assert request_data.method == RequestMethod.GET
    assert request_data.body == {}


def test_from_dict_with_body():
    request_data = RequestData.from_dict({'method': 'GET', 'body': {'foo': 'bar'}})
    assert request_data.method == RequestMethod.GET
    assert request_data.body == {'foo': 'bar'}
