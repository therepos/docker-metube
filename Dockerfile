FROM alexta69/metube:latest

RUN apk add --no-cache python3 py3-pip inotify-tools ffmpeg && \
    pip3 install mutagen

COPY postprocess.py /postprocess/postprocess.py
COPY cover.png /postprocess/cover.png
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /postprocess/postprocess.py /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
