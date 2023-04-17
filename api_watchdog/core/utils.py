import json
import shutil
import tempfile
from typing import Dict


def write_json_atomic(data: Dict, file_path: str):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        json.dump(data, temp_file)
        temp_file_path = temp_file.name

    shutil.move(temp_file_path, file_path)


def read_json_atomic(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        return json.load(file)
