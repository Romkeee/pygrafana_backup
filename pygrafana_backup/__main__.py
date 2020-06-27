import asyncio
import argparse
import logging
import urllib3

from .backup import backup
from .restore import restore
from .config import SSL_CHECK


def get_parser():
    logging_levels = ('debug', 'info', 'warning', 'error', 'critical')
    parser = argparse.ArgumentParser(prog='pygrafana-backup', description='Backups/Restores Grafana dashboards via api')
    parser.add_argument('-b', '--backup', action='store_true', help='Backup all dashboards')
    parser.add_argument('-r', '--restore', action='store_true', help='Restore all dashboards')
    parser.add_argument('-f', '--folder', type=str, help='Main folder path (default: ./backup)', default='./backup')
    parser.add_argument('-l', '--log', choices=logging_levels, default='info', help='Logging level (default: info)')
    return parser


def off_requests_warnings():
    logging.getLogger("requests").setLevel(logging.WARNING)
    if not SSL_CHECK:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    parser = get_parser()
    args = parser.parse_args()

    logging.basicConfig(level=args.log.upper(), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    off_requests_warnings()

    if args.backup and args.restore:
        parser.error("Arguments -b and -r can't be used together")
    elif args.backup or args.restore:
        loop = asyncio.get_event_loop()
        if args.backup:
            loop.run_until_complete(backup(args.folder))
        elif args.restore:
            loop.run_until_complete(restore(args.folder))


main()
