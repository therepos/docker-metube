#!/bin/sh

# Background postprocess watcher
python3 /app/postprocess.py &

# Run MeTube’s original entrypoint
exec /docker-entrypoint.sh "$@"
