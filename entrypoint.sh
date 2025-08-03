#!/bin/sh

# Start file watcher in background
/watch.sh &

# Hand over to MeTube's original entrypoint
exec "$@"
