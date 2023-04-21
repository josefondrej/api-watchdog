from datetime import datetime

import pytest
from sqlalchemy import create_engine, text

from api_watchdog.core.api_test_case_record import ApiTestCaseRecord
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult
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
    # select only table names, not sqlite sequence names
    sql = """
    SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """
    sql = text(sql)
    with initialized_engine.connect() as connection:
        result = connection.execute(sql).fetchall()
        assert result == [('api_test_case_records',)]


def test_initialize_with_non_empty_engine(database):
    database.initialize()


def test_insert_list_api_test_case_record(database):
    api_test_case_record = ApiTestCaseRecord(
        result=CompressedApiTestCaseResult(
            api_test_case_identifier='test_api_test_case_identifier',
            status=ApiTestCaseResultStatus.PASSED
        ),
        timestamp=datetime.now()
    )
    database.insert_api_test_case_record(api_test_case_record)
    records = database.list_api_test_case_records('test_api_test_case_identifier')
    assert len(records) == 1
    assert records[0].result.api_test_case_identifier == 'test_api_test_case_identifier'
    assert records[0].result.status == ApiTestCaseResultStatus.PASSED
