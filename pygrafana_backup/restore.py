import requests
import sys
import os
import json
import logging

from .config import HEADERS, SERVER, SSL_CHECK

logger = logging.getLogger(__name__)


def restore(folder_path):
    for file_path in os.scandir(folder_path):
        with open(file_path, 'r') as file:
            db_json = json.load(file)
            db_json['dashboard']['id'] = None
            db_title = db_json['dashboard']['title']

            try:
                response = requests.post(f"{SERVER}/api/dashboards/db", json=db_json, headers=HEADERS, verify=SSL_CHECK)
                response.raise_for_status()
                logger.info(f"Dashboard {db_title} restored from {file_path.path}")
            except requests.exceptions.HTTPError as e:
                logger.error(f"Grafana {e.response.status_code} error during {db_title} restore:\n{e.response.text}")
                sys.exit(1)
            except requests.exceptions.RequestException as e:
                logger.error(f"Error connecting to Grafana:\n{e}")
