#!/bin/sh

# Start postprocessor in background
python3 /app/postprocess.py &

# Run MeTube's original entrypoint
exec /docker-entrypoint.sh
