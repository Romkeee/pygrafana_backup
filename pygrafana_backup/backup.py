import json
import sys
import logging
import pathlib
import requests
from datetime import datetime
from os import path

from .config import HEADERS, SERVER, SSL_CHECK

logger = logging.getLogger(__name__)


def get_dashboards_uids():
    response = requests.get(f"{SERVER}/api/search?query=&type=dash-db", headers=HEADERS, verify=SSL_CHECK)
    response.raise_for_status()
    if not response.json():
        logger.info('No dashboards found to backup')
        sys.exit(0)
    return (db['uid'] for db in response.json())


def get_dashboard_by_uid(uid):
    return requests.get(f"{SERVER}/api/dashboards/uid/{uid}", headers=HEADERS, verify=SSL_CHECK)


def get_current_date():
    return datetime.today().strftime("%Y-%m-%d")


def create_sub_folder(main_folder_path):
    sub_folder_path = path.join(main_folder_path, get_current_date())
    pathlib.Path(sub_folder_path).mkdir(parents=True, exist_ok=True)
    return sub_folder_path


def save_dashboards(dashboards_uids, main_folder_path):
    sub_folder_path = create_sub_folder(main_folder_path)
    for uid in dashboards_uids:
        db = get_dashboard_by_uid(uid).json()
        db_title = db['dashboard']['title']
        db_path = path.join(sub_folder_path, db_title + '.json')
        with open(db_path, 'w') as file:
            json.dump(db, file, indent=2)
        logger.info(f'Dashboard {db_title} saved to {db_path}')


def backup(main_folder_path):
    try:
        dashboards_uids = get_dashboards_uids()
        save_dashboards(dashboards_uids, main_folder_path)
    except requests.exceptions.HTTPError as e:
        logger.error(f"Grafana {e.response.status_code} error during backup:\n{e.response.text}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Grafana:\n{e}")
    except PermissionError as e:
        logger.error(f"No permissions to create backup folder {main_folder_path}:{e}")
