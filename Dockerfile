FROM alexta69/metube:latest

RUN apk add --no-cache python3 py3-pip inotify-tools && \
    pip3 install mutagen

COPY postprocess.py /app/postprocess.py
COPY cover.png /app/cover.png

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["sh", "-c", "python3 /app/postprocess.py & exec python3 -u /app/main.py"]
