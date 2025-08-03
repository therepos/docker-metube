#!/bin/sh

# Start postprocessor in background
python3 /postprocess/postprocess.py &

# Start MeTube
exec python3 -u /srv/metube/main.py
