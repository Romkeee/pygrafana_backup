import aiohttp
import aiofiles
import asyncio
import json
import sys
import logging
import pathlib
import requests
from datetime import datetime
from os import path

from .config import HEADERS, SERVER, SSL_CHECK

logger = logging.getLogger(__name__)


def get_dbs_uids():
    response = requests.get(f"{SERVER}/api/search?query=&type=dash-db", headers=HEADERS, verify=SSL_CHECK)
    response.raise_for_status()
    if not response.json():
        logger.info('No dashboards found to backup')
        sys.exit(0)
    return (db['uid'] for db in response.json())


def get_current_date():
    return datetime.today().strftime("%Y-%m-%d")


def create_sub_folder(main_folder_path):
    sub_folder_path = path.join(main_folder_path, get_current_date())
    pathlib.Path(sub_folder_path).mkdir(parents=True, exist_ok=True)
    return sub_folder_path


async def save_db(session, db_uid, sub_folder_path):
    async with session.get(f"{SERVER}/api/dashboards/uid/{db_uid}", ssl=SSL_CHECK) as resp:
        db = await resp.json()
        db_title = db['dashboard']['title']
        db_path = path.join(sub_folder_path, db_title + '.json')
        async with aiofiles.open(db_path, mode='w') as file:
            await file.write(json.dumps(db, indent=2))
        logger.info(f'Dashboard {db_title} saved to {db_path}')


async def backup(main_folder_path):
    try:
        sub_folder_path = create_sub_folder(main_folder_path)
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            await asyncio.gather(
                *(save_db(session, db_uid, sub_folder_path) for db_uid in get_dbs_uids())
            )
    except aiohttp.ClientResponseError as e:
        logger.error(f"Grafana {e.status} error during backup:\n{e.message}")
        sys.exit(1)
    except aiohttp.ClientConnectionError as e:
        logger.error(f"Error connecting to Grafana:\n{e}")
        sys.exit(1)
    except PermissionError as e:
        logger.error(f"No permissions to create backup folder {main_folder_path}:{e}")
