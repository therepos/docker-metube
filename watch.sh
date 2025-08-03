#!/bin/sh

WATCH_DIR="/downloads"

inotifywait -m -e close_write,moved_to --format "%w%f" "$WATCH_DIR" | while read FILE; do
  case "$FILE" in
    *.mp3|*.m4a)
      echo "Post-processing $FILE"
      python3 /app/postprocess.py "$FILE"
      ;;
  esac
done
