import requests
import os
import json
import logging

from .config import HEADERS, SERVER

logger = logging.getLogger(__name__)


def restore(folder_path):
    for file_path in os.scandir(folder_path):
        with open(file_path, 'r') as file:
            db_json = json.load(file)
            db_json['dashboard']['id'] = None
            response = requests.post(f"{SERVER}/api/dashboards/db", json=db_json, headers=HEADERS)
            response_code = response.status_code
            if response_code == 200:
                logger.info(f"Dashboard {file_path.path} restored")
            else:
                logger.error(f"Can't restore {file_path.path}. Exit code: {response_code}. Error: {response.text}")
