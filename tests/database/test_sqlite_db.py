import pytest
from sqlalchemy import create_engine, text

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_result import ApiTestCaseResult
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult
from api_watchdog.core.request_data import RequestData
from api_watchdog.core.request_method import RequestMethod
from api_watchdog.core.response_data import ResponseData
from api_watchdog.database.sqlite_db import SqliteDb


@pytest.fixture
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture
def initialized_engine(engine):
    SqliteDb(engine).initialize()
    return engine


@pytest.fixture
def database(engine) -> SqliteDb:
    return SqliteDb(engine)


def test_initialize_tables_exist(initialized_engine):
    sql = """
    SELECT name FROM sqlite_master WHERE type='table';
    """
    sql = text(sql)
    with initialized_engine.connect() as connection:
        result = connection.execute(sql).fetchall()
        assert result == [('api_test_cases',), ('api_test_case_results',)]


def test_initialize_with_non_empty_engine(database):
    database.initialize()


def test_insert_load_api_test_case(database: SqliteDb):
    api_test_case = ApiTestCase(
        identifier='test',
        url='http://example.com',
        request_data=RequestData(
            method=RequestMethod.GET,
            body={'test': 'test'},
        ),
        expected_response_data=ResponseData(
            status_code=200,
            body={'test': 'test'},
        ),
    )
    database.insert_api_test_case(api_test_case)
    retrieved_test_case = database.load_api_test_case(api_test_case.identifier)
    assert api_test_case.identifier == retrieved_test_case.identifier
    assert api_test_case.url == retrieved_test_case.url
    assert api_test_case.request_data.method == retrieved_test_case.request_data.method
    assert api_test_case.request_data.body == retrieved_test_case.request_data.body
    assert api_test_case.expected_response_data.status_code == retrieved_test_case.expected_response_data.status_code
    assert api_test_case.expected_response_data.body == retrieved_test_case.expected_response_data.body


def test_insert_load_compressed_api_test_case_result(database: SqliteDb):
    compressed_api_test_case_result = CompressedApiTestCaseResult(
        api_test_case_identifier='test',
        status=ApiTestCaseResultStatus.PASSED,
    )
    database.insert_compressed_api_test_case_result(compressed_api_test_case_result)
    (timestamp, retrieved_compressed_api_test_case_result), *_ = database.load_compressed_api_test_case_results(
        compressed_api_test_case_result.api_test_case_identifier)
    assert compressed_api_test_case_result.api_test_case_identifier == retrieved_compressed_api_test_case_result.api_test_case_identifier
    assert compressed_api_test_case_result.status == retrieved_compressed_api_test_case_result.status


def test_insert_load_api_test_case_result(database: SqliteDb):
    api_test_case_result = ApiTestCaseResult(
        api_test_case=ApiTestCase(
            identifier='test',
            url='http://example.com',
            request_data=RequestData(
                method=RequestMethod.GET,
                body={'test': 'test'},
            ),
            expected_response_data=ResponseData(
                status_code=200,
                body={'test': 'test'},
            ),
        ),
        status=ApiTestCaseResultStatus.PASSED,
        response_data=ResponseData(
            status_code=200,
            body={'test': 'test'},
        ),
    )
    database.insert_api_test_case_result(api_test_case_result)
    (timestamp, retrieved_api_test_case_result), *_ = database.load_api_test_case_results(
        api_test_case_result.api_test_case.identifier)

    assert api_test_case_result.api_test_case.identifier == retrieved_api_test_case_result.api_test_case.identifier
    assert api_test_case_result.api_test_case.url == retrieved_api_test_case_result.api_test_case.url
    assert api_test_case_result.api_test_case.request_data.method == retrieved_api_test_case_result.api_test_case.request_data.method
    assert api_test_case_result.api_test_case.request_data.body == retrieved_api_test_case_result.api_test_case.request_data.body
    assert api_test_case_result.api_test_case.expected_response_data.status_code == retrieved_api_test_case_result.api_test_case.expected_response_data.status_code
    assert api_test_case_result.api_test_case.expected_response_data.body == retrieved_api_test_case_result.api_test_case.expected_response_data.body
    assert api_test_case_result.status == retrieved_api_test_case_result.status
    assert api_test_case_result.response_data.status_code == retrieved_api_test_case_result.response_data.status_code
    assert api_test_case_result.response_data.body == retrieved_api_test_case_result.response_data.body
    assert api_test_case_result.exception == retrieved_api_test_case_result.exception
