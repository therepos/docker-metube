FROM alexta69/metube:latest

# Install dependencies
RUN apk add --no-cache ffmpeg inotify-tools python3 py3-pip build-base libffi-dev \
 && pip install mutagen

# Set working directory
WORKDIR /app

# Copy custom scripts and assets
COPY postprocess.py cover.png ./

# Run postprocess in background, then start MeTube
CMD ["sh", "-c", "python3 /app/postprocess.py & exec docker-entrypoint.sh"]
