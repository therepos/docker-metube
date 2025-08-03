FROM alexta69/metube:latest

RUN apk add --no-cache ffmpeg python3 py3-pip build-base libffi-dev \
 && pip install mutagen watchdog

WORKDIR /app

COPY postprocess.py cover.png entrypoint.sh ./
RUN chmod +x /app/entrypoint.sh

# Use our wrapper, but keep original entrypoint intact
ENTRYPOINT ["/app/entrypoint.sh"]
