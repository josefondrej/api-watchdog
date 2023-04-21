import json
from typing import List

from sqlalchemy import Engine, text

from api_watchdog.core.api_test_case_record import ApiTestCaseRecord
from api_watchdog.database.db_base import DbBase


class SqliteDb(DbBase):
    def __init__(self, engine: Engine):
        self._engine = engine
        self.initialize()

    def __str__(self):
        return f'SqliteDb({self._engine.url})'

    def initialize(self):
        create_api_test_case_records_table_sql = """
        CREATE TABLE IF NOT EXISTS api_test_case_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_test_case_identifier TEXT NOT NULL,
            serialized_api_test_case_record TEXT NOT NULL
        );
        """

        with self._engine.connect() as connection:
            connection.execute(text(create_api_test_case_records_table_sql))

    def insert_api_test_case_record(self, api_test_case_record: ApiTestCaseRecord):
        api_test_case_identifier = api_test_case_record.result.api_test_case_identifier
        serialized_api_test_case_record = json.dumps(api_test_case_record.to_dict())

        sql = f"INSERT INTO api_test_case_records (api_test_case_identifier, serialized_api_test_case_record) " \
              f"VALUES (:api_test_case_identifier, :serialized_api_test_case_record)"
        sql_executable = text(sql)

        with self._engine.connect() as connection:
            connection.execute(
                statement=sql_executable,
                parameters=dict(
                    api_test_case_identifier=api_test_case_identifier,
                    serialized_api_test_case_record=serialized_api_test_case_record
                )
            )
            connection.commit()

    def list_api_test_case_records(self, api_test_case_identifier: str) -> List[ApiTestCaseRecord]:
        sql = f"SELECT serialized_api_test_case_record FROM api_test_case_records WHERE api_test_case_identifier = :api_test_case_identifier"
        sql_executable = text(sql)

        with self._engine.connect() as connection:
            results = connection.execute(
                statement=sql_executable,
                parameters=dict(api_test_case_identifier=api_test_case_identifier)
            ).fetchall()
            return [ApiTestCaseRecord.from_dict(json.loads(result[0])) for result in results]
