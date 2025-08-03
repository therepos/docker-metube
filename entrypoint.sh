#!/bin/bash

# Original MeTube entrypoint with post-processing hook
# This script extends the original functionality

# Set up post-processing hook
export METUBE_POST_PROCESSOR="/app/postprocess.py"

# Function to process downloaded files
process_downloaded_file() {
    local file_path="$1"
    if [[ -f "$file_path" && "$file_path" =~ \.(mp3|flac|mp4|m4a|ogg)$ ]]; then
        echo "Post-processing: $file_path"
        python3 /app/postprocess.py "$file_path"
    fi
}

# Monitor the download directory for new files
monitor_downloads() {
    local download_dir="/downloads"
    
    # Use inotify to monitor for new files
    if command -v inotifywait >/dev/null 2>&1; then
        inotifywait -m -r -e close_write --format '%w%f' "$download_dir" | while read file; do
            if [[ "$file" =~ \.(mp3|flac|mp4|m4a|ogg)$ ]]; then
                sleep 1  # Give the file system a moment to settle
                process_downloaded_file "$file"
            fi
        done &
    else
        # Fallback: periodically scan for new files
        while true; do
            find "$download_dir" -name "*.mp3" -o -name "*.flac" -o -name "*.mp4" -o -name "*.m4a" -o -name "*.ogg" | while read file; do
                # Simple timestamp check - process files modified in the last minute
                if [[ $(find "$file" -mmin -1 2>/dev/null) ]]; then
                    process_downloaded_file "$file"
                fi
            done
            sleep 30
        done &
    fi
}

# Install inotify-tools if not present
if ! command -v inotifywait >/dev/null 2>&1; then
    echo "Installing inotify-tools for file monitoring..."
    apt-get update && apt-get install -y inotify-tools
fi

# Start the monitoring in the background
monitor_downloads

# Execute the original MeTube entrypoint
exec python3 /app/metube/main.py