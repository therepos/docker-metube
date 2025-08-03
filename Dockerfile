FROM alexta69/metube:latest

RUN apk add --no-cache ffmpeg inotify-tools python3 py3-pip build-base libffi-dev \
 && pip install mutagen

COPY postprocess.py cover.png /app/

RUN chmod +x /app/postprocess.py

# Use CMD to run your watcher then MeTube's original startup
CMD ["sh", "-c", "python3 /app/postprocess.py & exec ./docker-entrypoint.sh"]
