FROM alexta69/metube:latest

# Install deps
RUN apk add --no-cache ffmpeg python3 py3-pip build-base libffi-dev \
 && pip install mutagen watchdog

# Create app dir and copy files
WORKDIR /app
COPY postprocess.py cover.png start.sh ./

RUN chmod +x /app/start.sh

# Start MeTube + postprocess
ENTRYPOINT ["/app/start.sh"]
