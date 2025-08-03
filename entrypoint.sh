#!/bin/sh

# Force yt-dlp to call our script after each download
ARGS="--download-archive /downloads/archive.txt --exec python3 /postprocess/postprocess.py {}"

# Run the actual MeTube app
exec python3 app/main.py $ARGS
