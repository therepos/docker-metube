FROM alexta69/metube:latest

RUN apk add --no-cache ffmpeg inotify-tools python3 py3-pip build-base libffi-dev \
 && pip install mutagen

WORKDIR /app

COPY postprocess.py cover.png ./

CMD ["sh", "-c", "python3 /app/postprocess.py & exec /usr/local/bin/docker-entrypoint.sh"]
