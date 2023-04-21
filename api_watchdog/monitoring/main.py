import logging
import time
from pathlib import Path
from typing import Union

from sqlalchemy import create_engine

import api_watchdog.config as config
from api_watchdog.core.api_test_case_result_status import ApiTestCaseResultStatus
from api_watchdog.core.config import Config
from api_watchdog.core.main import run_api_test_case
from api_watchdog.database.sqlite_db import SqliteDb

logger = logging.getLogger(__name__)


def run_monitoring(config_file_path: Union[Path, str], database: SqliteDb):
    logger.info(f'Starting monitoring; Config file: {config_file_path}; Database: {database}')
    while True:
        logger.info('Reading config file')
        config = Config.from_file(config_file_path)

        logger.info('Running api test cases')
        for api_test_case in config.api_test_cases:
            api_test_case_record = run_api_test_case(api_test_case)
            database.insert_api_test_case_record(api_test_case_record)
            if api_test_case_record.result.status != ApiTestCaseResultStatus.PASSED:
                logger.error(f'Api test case failed: {api_test_case_record.to_dict()}')
                # TODO: Connect to some notification system here

        logger.info(f'Waiting {config.request_frequency_sec} seconds')
        time.sleep(config.request_frequency_sec)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    sqlite_engine = create_engine(config.DATABASE_CONNECTION_STRING)
    database = SqliteDb(sqlite_engine)

    run_monitoring(config_file_path=config.CONFIG_FILE_PATH, database=database)
