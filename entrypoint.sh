#!/bin/sh

# Start postprocess in background
python3 /app/postprocess.py &

# Now exec MeTube's original entrypoint with any passed args
exec /docker-entrypoint.sh "$@"
