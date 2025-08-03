FROM alexta69/metube:latest

RUN apk add --no-cache python3 py3-pip ffmpeg inotify-tools && \
    pip3 install mutagen

COPY postprocess.py /app/
COPY cover.png /app/
COPY watch.sh /watch.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh /watch.sh

ENTRYPOINT ["/entrypoint.sh"]
