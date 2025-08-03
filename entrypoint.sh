#!/bin/sh

# Create log file if it doesn't exist
echo "[ENTRYPOINT $(date)] Starting entrypoint.sh" >> /downloads/postprocess.log

# Force yt-dlp to trigger postprocess.py
ARGS="--download-archive /downloads/archive.txt --exec python3 /postprocess/postprocess.py {}"

echo "[ENTRYPOINT $(date)] Running MeTube with args: $ARGS" >> /downloads/postprocess.log

exec python3 app/main.py $ARGS
