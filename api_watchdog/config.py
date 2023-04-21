import os

DATA_DIR = os.environ.get('API_WATCHDOG_DATA_DIR', '/tmp')
DATABASE_CONNECTION_STRING = f'sqlite:///{DATA_DIR}/database.db'
CONFIG_FILE_PATH = f'{DATA_DIR}/config.json'
