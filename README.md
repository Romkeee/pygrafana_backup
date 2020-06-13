# pygrafana_backup

Python based utility designed to backup/restore Grafana dashboards via API.

## Prerequisites

```
python >= python3.7
requests (script was created using 2.23.0)
```

## Usage

```shell script
python -m pygrafana_backup -h
usage: pygrafana-backup [-h] [-b] [-r] [-f FOLDER] [-l {debug,info,warning,error,critical}]

Backups/Restores Grafana dashboards via api

optional arguments:
  -h, --help                 show this help message and exit
  -b, --backup               Backup all dashboards
  -r, --restore              Restore all dashboards
  -f FOLDER, --folder FOLDER Main folder path (default: ./backup)
  -l {debug,info,warning,error,critical}, --log {debug,info,warning,error,critical} Logging level (default: info)
```

#### Examples

Backup
```shell script
export SERVER='https://grafana.lab:3000'
export API_KEY='xxx'
python -m pygrafana_backup -b -f '/backups/grafana/'
```

Restore
```shell script
export SERVER='https://grafana.lab:3000'
export API_KEY='xxx'
python -m pygrafana_backup -r -f '/backups/grafana/2020-06-05/'
```

## Info

####General
SSL by default is disabled but can be enabled by providing environment variable:

```shell script
export SSL_CHECK=True
```

####Restore
Restore procedure designed to upload dashboards only if Grafana host doesn't have the same dashboards already.
Otherwise API just creates a new version on top of existing dashboard.  

If you wish to import dashboard by hands then you need to delete 'meta' section and 'dashboard' key ending with such json:
```json
{
  "annotations": {},
  "editable": true,
  "gnetId": null,
  "graphTooltip": 0,
  "id": 56,
  "links": [],
  "panels": [],
  "schemaVersion": 25,
  "style": "dark",
  "tags": [],
  "templating": {},
  "time": {},
  "timepicker": {},
  "timezone": "",
  "title": "nginx",
  "uid": "788t08zGk",
  "version": 1
}
```


