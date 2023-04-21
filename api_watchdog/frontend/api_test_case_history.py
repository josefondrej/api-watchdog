from typing import List

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_record import ApiTestCaseRecord


class ApiTestCaseHistory:
    def __init__(self, test_case: ApiTestCase, records: List[ApiTestCaseRecord]):
        self.test_case = test_case
        self.records = sorted(records, key=lambda record: record.timestamp, reverse=True)

    @property
    def status(self) -> str:
        last_records = self.records[:100]
        if len(self.records) == 0:
            return 'warning'

        passed_percentage = sum(1 for record in last_records if record.result.status.value == 'PASSED') / len(
            last_records)
        if passed_percentage == 1:
            return 'success'
        elif passed_percentage > 0.95:
            return 'warning'
        else:
            return 'danger'
