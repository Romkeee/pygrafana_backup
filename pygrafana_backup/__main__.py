import argparse
import logging

from .backup import backup
from .restore import restore


def get_parser():
    logging_levels = ('debug', 'info', 'warning', 'error', 'critical')
    parser = argparse.ArgumentParser(prog='pygrafana-backup', description='Backups/Restores Grafana dashboards via api')
    parser.add_argument('-b', '--backup', action='store_true', help='Backup all dashboards')
    parser.add_argument('-r', '--restore', action='store_true', help='Restore all dashboards')
    parser.add_argument('-f', '--folder', type=str, help='Main folder path', default='./backup')
    parser.add_argument('-l', '--log', choices=logging_levels, default='info', help='Logging level (default: info)')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    logging.basicConfig(level=args.log.upper(), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger("requests").setLevel(logging.WARNING)

    if args.backup and args.restore:
        parser.error("Arguments -b and -r can't be used together")
    elif args.backup:
        backup(args.folder)
    elif args.restore:
        restore(args.folder)


main()
