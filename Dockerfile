FROM alexta69/metube:latest

RUN apk add --no-cache python3 py3-pip ffmpeg inotify-tools && \
    pip3 install mutagen

COPY postprocess.py /app/
COPY cover.png /app/
COPY entrypoint.sh /entrypoint.sh
COPY watch.sh /watch.sh
RUN chmod +x /entrypoint.sh /watch.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["./start.sh"]
