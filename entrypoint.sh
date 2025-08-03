#!/bin/sh

SRC="/downloads"
DEST="/mnt/sec/media/music"

# Start MeTube in background
/start.sh &

echo "Watching $SRC..."

# Run the watcher in foreground
inotifywait -m -e close_write,moved_to --format '%w%f' "$SRC" | while read FILE; do
  case "$FILE" in
    *.mp3|*.m4a)
      echo "Post-processing $FILE"
      TMP="/tmp/$(basename "$FILE")"
      cp "$FILE" "$TMP"
      python3 /app/postprocess.py "$TMP" && mv "$TMP" "$DEST/"
      echo "Moved to $DEST"
      ;;
  esac
done
