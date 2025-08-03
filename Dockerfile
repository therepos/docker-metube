FROM alexta69/metube:latest

RUN apk add --no-cache ffmpeg python3 py3-pip build-base libffi-dev \
 && pip install mutagen watchdog

COPY postprocess.py /app/postprocess.py
COPY cover.png /app/cover.png

# Optional: create a simple startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENTRYPOINT ["/app/start.sh"]
