from datetime import datetime
from typing import List, Tuple, Optional

from api_watchdog.core.api_test_case import ApiTestCase
from api_watchdog.core.api_test_case_result import ApiTestCaseResult
from api_watchdog.core.compressed_api_test_case_result import CompressedApiTestCaseResult
from api_watchdog.core.decompress_api_test_case_result import decompress


class DbBase:
    def insert_api_test_case(self, api_test_case: ApiTestCase):
        raise NotImplementedError

    def load_api_test_case(self, api_test_case_identifier: str) -> Optional[ApiTestCase]:
        raise NotImplementedError

    def insert_compressed_api_test_case_result(self, compressed_api_test_case_result: CompressedApiTestCaseResult):
        raise NotImplementedError

    def load_compressed_api_test_case_results(self, api_test_case_identifier: str) -> List[
        Tuple[datetime, CompressedApiTestCaseResult]]:
        raise NotImplementedError

    def insert_api_test_case_result(self, api_test_case_result: ApiTestCaseResult):
        api_test_case = api_test_case_result.api_test_case
        compressed_api_test_case_result = api_test_case_result.compress()
        self.insert_api_test_case(api_test_case)
        self.insert_compressed_api_test_case_result(compressed_api_test_case_result)

    def load_api_test_case_results(self, api_test_case_identifier: str) -> List[Tuple[datetime, ApiTestCaseResult]]:
        compressed_api_test_case_results_with_timestamps = self.load_compressed_api_test_case_results(
            api_test_case_identifier)
        api_test_case = self.load_api_test_case(api_test_case_identifier)
        return [
            (timestamp, decompress(compressed_api_test_case_result, [api_test_case]))
            for timestamp, compressed_api_test_case_result in compressed_api_test_case_results_with_timestamps
        ]
