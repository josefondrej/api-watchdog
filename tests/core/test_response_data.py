from api_watchdog.core.response_data import ResponseData


def test_to_dict():
    response_data = ResponseData(200)
    assert response_data.to_dict() == {'status_code': 200, 'body': {}}


def test_to_dict_with_body():
    response_data = ResponseData(200, {'foo': 'bar'})
    assert response_data.to_dict() == {'status_code': 200, 'body': {'foo': 'bar'}}


def test_from_dict():
    response_data = ResponseData.from_dict({'status_code': 200, 'body': {}})
    assert response_data.status_code == 200
    assert response_data.body == {}


def test_from_dict_with_body():
    response_data = ResponseData.from_dict({'status_code': 200, 'body': {'foo': 'bar'}})
    assert response_data.status_code == 200
    assert response_data.body == {'foo': 'bar'}
