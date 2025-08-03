FROM alexta69/metube:latest

RUN apk add --no-cache ffmpeg inotify-tools python3 py3-pip \
 && pip install mutagen

COPY postprocess.py cover.png /app/
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
