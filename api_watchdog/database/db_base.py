from typing import List

from api_watchdog.core.api_test_case_record import ApiTestCaseRecord


class DbBase:
    def insert_api_test_case_record(self, api_test_case_record: ApiTestCaseRecord):
        raise NotImplementedError('Has to be implemented by subclass')

    def list_api_test_case_records(self, api_test_case_identifier: str) -> List[ApiTestCaseRecord]:
        raise NotImplementedError('Has to be implemented by subclass')
