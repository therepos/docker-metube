#!/bin/sh

SRC="/downloads"
DEST="/mnt/sec/media/music"

echo "Watcher started on $SRC"

inotifywait -m -e close_write,moved_to --format '%w%f' "$SRC" | while read FILE; do
  case "$FILE" in
    *.mp3|*.m4a)
      echo "Post-processing $FILE"
      TMP="/tmp/$(basename "$FILE")"
      cp "$FILE" "$TMP"
      python3 /postprocess.py "$TMP" && mv "$TMP" "$DEST/"
      echo "Moved to $DEST"
      ;;
  esac
done
