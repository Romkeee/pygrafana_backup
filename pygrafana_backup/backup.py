import json
import logging
import pathlib
import requests
from datetime import datetime

from .config import HEADERS, SERVER

logger = logging.getLogger(__name__)


def get_dashboards_uids():
    all_dashboards = requests.get(f"{SERVER}/api/search?query=&type=dash-db", headers=HEADERS)
    return [db['uid'] for db in all_dashboards.json()]


def get_dashboard_by_uid(uid):
    return requests.get(f"{SERVER}/api/dashboards/uid/{uid}", headers=HEADERS)


def get_current_date():
    return datetime.today().strftime("%Y-%m-%d")


def create_sub_folder(main_folder_path):
    sub_folder_path = f"{main_folder_path}/{get_current_date()}"
    pathlib.Path(sub_folder_path).mkdir(parents=True, exist_ok=True)
    return sub_folder_path


def save_dashboards(dashboards_uids, main_folder_path):
    sub_folder_path = create_sub_folder(main_folder_path)
    for uid in dashboards_uids:
        db = get_dashboard_by_uid(uid).json()
        db_title = db['dashboard']['title']
        db_path = f"{sub_folder_path}/{db_title}.json"
        with open(db_path, 'w') as file:
            json.dump(db, file, indent=2)
        logger.info(f'Dashboard {db_title} saved to {db_path}')


def backup(main_folder_path):
    dashboards_uids = get_dashboards_uids()
    save_dashboards(dashboards_uids, main_folder_path)
