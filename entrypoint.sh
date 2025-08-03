#!/bin/sh

# Run postprocessor in background
python3 /postprocess/postprocess.py &

# Start MeTube the way the image expects
/docker-entrypoint.sh
