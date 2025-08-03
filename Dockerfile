FROM alexta69/metube:latest

RUN apk add --no-cache ffmpeg python3 py3-pip build-base libffi-dev \
 && pip install mutagen watchdog

WORKDIR /wrapper
COPY entrypoint.sh postprocess.py cover.png ./
RUN sed -i 's/\r$//g' entrypoint.sh postprocess.py && chmod +x entrypoint.sh

ENTRYPOINT ["/wrapper/entrypoint.sh"]
