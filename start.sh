#!/bin/sh

# Run postprocess.py in background
python3 /app/postprocess.py &

# Run original entrypoint (metube)
exec /docker-entrypoint.sh
