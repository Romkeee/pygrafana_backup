import aiohttp
import aiofiles
import sys
import os
import json
import logging
from collections import namedtuple

from .config import HEADERS, SERVER, SSL_CHECK

logger = logging.getLogger(__name__)


async def exit_if_db_exists(dashboard, session):
    async with session.post(f"{SERVER}/api/dashboards/uid/{dashboard.uid}", ssl=SSL_CHECK) as response:
        if response.status == 200:
            logger.error(f"Dashboard with the same uid found: {dashboard.uid}."
                         f" Name: {dashboard.title}. Exiting restore.")
            sys.exit(1)


async def upload_db(dashboard):
    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            await exit_if_db_exists(dashboard, session)
            dashboard.json['dashboard']['id'] = None
            async with session.post(f"{SERVER}/api/dashboards/db", json=dashboard.json, ssl=SSL_CHECK) as response:
                response.raise_for_status()
                logger.info(f"Dashboard {dashboard.title} restored from {dashboard.file_path.path}")
    except aiohttp.ClientResponseError as e:
        logger.error(f"Grafana '{e.status}' error code during {dashboard.title} restore:\n{e.message}")
        sys.exit(1)
    except aiohttp.ClientConnectionError as e:
        logger.error(f"Error connecting to Grafana:\n{e}")
        sys.exit(1)


async def restore(folder_path):
    for db_file_path in os.scandir(folder_path):
        async with aiofiles.open(db_file_path, mode='r') as file:
            db_file = await file.read()
            db_json = json.loads(db_file)
            Dashboard = namedtuple('Dashboard', 'json uid title file_path')
            dashboard = Dashboard(
                db_json,
                db_json['dashboard']['uid'],
                db_json['dashboard']['title'],
                db_file_path
            )
            await upload_db(dashboard)
