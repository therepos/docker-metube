#!/bin/sh

echo "[ENTRYPOINT $(date)] Starting watcher" >> /app/postprocess.log

# Start the original MeTube startup command in the background
/sbin/tini -- /start.sh &
METUBE_PID=$!

# Start watcher
inotifywait -m /downloads -e close_write |
while read path action file; do
  if echo "$file" | grep -Ei '\.mp3$|\.m4a$'; then
    echo "[WATCHER $(date)] Detected $file – running postprocess.py" >> /app/postprocess.log
    python3 /app/postprocess.py "/downloads/$file" >> /app/postprocess.log 2>&1
  fi
done &

wait $METUBE_PID
