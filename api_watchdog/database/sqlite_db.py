import json
from datetime import datetime
from typing import List, Tuple, Optional

from sqlalchemy import Engine, text

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult
from api_watchdog.database.db_base import DbBase


class SqliteDb(DbBase):
    def __init__(self, engine: Engine):
        self._engine = engine
        self.initialize()

    def initialize(self):
        # create tables if they don't exist:
        # api_test_cases(identfier str, timestamp_inserted: datetime, serialized_case: str),
        # api_test_case_results(api_test_case_identifier str, timestamp_inserted: datetime, serialized_result: str)
        create_api_test_case_table_sql = """
        CREATE TABLE IF NOT EXISTS api_test_cases (
            identifier TEXT NOT NULL,
            timestamp_inserted DATETIME NOT NULL,
            serialized_api_test_case TEXT NOT NULL,
            PRIMARY KEY (identifier)
        );
        """

        create_api_test_case_results_table_sql = """
        CREATE TABLE IF NOT EXISTS api_test_case_results (
            api_test_case_identifier TEXT NOT NULL,
            timestamp_inserted DATETIME NOT NULL,
            serialized_api_test_case_result TEXT NOT NULL,
            PRIMARY KEY (api_test_case_identifier, timestamp_inserted)
        );
        """

        with self._engine.connect() as connection:
            connection.execute(text(create_api_test_case_table_sql))
            connection.execute(text(create_api_test_case_results_table_sql))

    def insert_api_test_case(self, api_test_case: ApiTestCase):
        sql = f"INSERT INTO api_test_cases (identifier, timestamp_inserted, serialized_api_test_case) " \
              f"VALUES ('{api_test_case.identifier}', '{datetime.now()}', '{json.dumps(api_test_case.to_dict())}')"
        sql_executable = text(sql)

        with self._engine.connect() as connection:
            connection.execute(sql_executable)
            connection.commit()

    def load_api_test_case(self, api_test_case_identifier: str) -> Optional[ApiTestCase]:
        sql = f"SELECT serialized_api_test_case FROM api_test_cases WHERE identifier = '{api_test_case_identifier}'"
        sql_executable = text(sql)

        with self._engine.connect() as connection:
            result = connection.execute(
                statement=sql_executable
            ).fetchone()
            if result is None:
                return None
            return ApiTestCase.from_dict(json.loads(result[0]))

    def insert_compressed_api_test_case_result(self, compressed_api_test_case_result: CompressedApiTestCaseResult):
        sql = f"INSERT INTO api_test_case_results (api_test_case_identifier, timestamp_inserted, serialized_api_test_case_result) " \
              f"VALUES ('{compressed_api_test_case_result.api_test_case_identifier}', '{datetime.now().isoformat()}', '{json.dumps(compressed_api_test_case_result.to_dict())}')"
        sql_executable = text(sql)

        with self._engine.connect() as connection:
            connection.execute(sql_executable)
            connection.commit()

    def load_compressed_api_test_case_results(self, api_test_case_identifier: str) -> List[
        Tuple[datetime, CompressedApiTestCaseResult]]:
        sql = f"SELECT timestamp_inserted, serialized_api_test_case_result FROM api_test_case_results WHERE api_test_case_identifier = '{api_test_case_identifier}'"
        sql_executable = text(sql)

        with self._engine.connect() as connection:
            result = connection.execute(sql_executable).fetchall()
            return [
                (
                    datetime.fromisoformat(row[0]),
                    CompressedApiTestCaseResult.from_dict(json.loads(row[1]))
                )
                for row in result]
