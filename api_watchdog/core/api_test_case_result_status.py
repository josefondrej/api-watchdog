from enum import Enum


class ApiTestCaseResultStatus(Enum):
    """Enum for test case result status."""
    PASSED = 'PASSED'
    FAILED = 'FAILED'
    ERROR = 'ERROR'
