FROM alexta69/metube:latest

RUN apt update && apt install -y python3-pip ffmpeg && \
    pip3 install mutagen

COPY postprocess.py /app/
COPY cover.png /app/

ENV POSTPROCESS_COMMAND="python3 /app/postprocess.py \"{}\""
