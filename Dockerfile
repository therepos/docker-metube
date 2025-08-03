FROM alexta69/metube:latest

RUN apk add --no-cache python3 py3-pip ffmpeg inotify-tools supervisor && \
    pip3 install mutagen

COPY postprocess.py /postprocess.py
COPY cover.png /cover.png
COPY watcher.sh /watcher.sh
COPY supervisord.conf /etc/supervisord.conf

RUN chmod +x /watcher.sh

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
