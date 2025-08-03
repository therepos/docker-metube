#!/bin/sh

# Start postprocessor in background
python3 /postprocess/postprocess.py &

# Start MeTube (default behavior)
python3 -u /app/main.py
