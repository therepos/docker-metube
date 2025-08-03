FROM alexta69/metube:latest

RUN apk add --no-cache python3 py3-pip ffmpeg inotify-tools && \
    pip3 install mutagen

COPY postprocess.py /postprocess.py
COPY cover.png /cover.png
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
