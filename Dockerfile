FROM alexta69/metube:latest

RUN apk add --no-cache python3 py3-pip ffmpeg inotify-tools && \
    pip3 install mutagen

COPY postprocess/postprocess.py /postprocess/postprocess.py
COPY postprocess/cover.png /postprocess/cover.png
COPY postprocess/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
