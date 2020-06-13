FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONUNBUFFERED=true

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir -p /opt/pybackup/ \
 && chown 1000:1000 /opt/pybackup \
 && groupadd -g 1000 pybackup \
 && useradd -d /opt/pybackup -u 1000 -g 1000 -s /bin/bash pybackup

WORKDIR /opt/pybackup
COPY --chown=1000:1000 pygrafana_backup ./pygrafana_backup/

USER pybackup

ENTRYPOINT ["python", "-m", "pygrafana_backup"]
CMD ["-b"]