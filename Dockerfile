FROM alexta69/metube:latest

RUN apk add --no-cache python3 py3-pip ffmpeg inotify-tools && \
    pip3 install mutagen

COPY postprocess.py /app/postprocess.py
COPY cover.png /app/cover.png
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
