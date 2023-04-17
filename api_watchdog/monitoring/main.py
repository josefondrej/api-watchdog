import logging
import time
from pathlib import Path
from typing import Union

from api_watchdog.core.config import Config
from api_watchdog.core.main import run_api_test_case
from api_watchdog.core.utils import read_json_atomic

logger = logging.getLogger(__name__)


def run_monitoring(config_file_path: Union[Path, str]):
    logger.info(f'Starting monitoring with config file: {config_file_path}')
    while True:
        logger.info('Reading config file')
        config = Config.from_dict(read_json_atomic(config_file_path))

        logger.info('Running api test cases')
        for api_test_case in config.api_test_cases:
            api_test_case_result = run_api_test_case(api_test_case)
            print(api_test_case_result)  # TODO: Save to database

        logger.info(f'Waiting {config.request_frequency_sec} seconds')
        time.sleep(config.request_frequency_sec)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    CONFIG_FILE_PATH = Path(__file__).parent.parent.parent / 'data' / 'config.json'
    run_monitoring(config_file_path=CONFIG_FILE_PATH)
