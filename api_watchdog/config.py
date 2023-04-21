from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
DATABASE_CONNECTION_STRING = f'sqlite:///{DATA_DIR / "database.db"}'
CONFIG_FILE_PATH = DATA_DIR / 'config.json'
