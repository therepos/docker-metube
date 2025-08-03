FROM alexta69/metube:latest

RUN apk add --no-cache python3 py3-pip ffmpeg && \
    pip3 install mutagen

COPY postprocess.py /app/
COPY cover.png /app/

ENV POSTPROCESS_COMMAND="python3 /app/postprocess.py \"{}\""
