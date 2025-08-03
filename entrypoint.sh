#!/bin/sh

# Start your watcher
python3 /app/postprocess.py &

# Call MeTube's original entrypoint
exec /sbin/tini -g -- ./docker-entrypoint.sh "$@"
