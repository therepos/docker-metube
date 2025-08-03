FROM alexta69/metube:latest

# Install required packages
RUN apk add --no-cache ffmpeg python3 py3-pip build-base libffi-dev \
 && pip install mutagen watchdog

# Set working directory
WORKDIR /app

# Copy files explicitly
COPY postprocess.py /app/postprocess.py
COPY cover.png /app/cover.png
COPY entrypoint.sh /app/entrypoint.sh

# Ensure correct line endings and permissions
RUN chmod +x /app/entrypoint.sh && dos2unix /app/entrypoint.sh || true

# Override entrypoint safely
ENTRYPOINT ["/app/entrypoint.sh"]
