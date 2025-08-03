#!/bin/sh
# wrapper entrypoint

# launch your postprocessor in background
python3 /wrapper/postprocess.py &

# pass control to MeTube's official entrypoint
exec /docker-entrypoint.sh "$@"
