FROM alexta69/metube:latest

USER root

# Install minimal dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    inotify-tools

# Use pre-built wheels when possible
RUN pip3 install --upgrade pip

# Install packages one by one for better error tracking
RUN pip3 install --no-cache-dir mutagen==1.47.0
RUN pip3 install --no-cache-dir --only-binary=all Pillow==10.4.0

# Copy custom files
COPY postprocess.py /app/postprocess.py
COPY cover.png /app/cover.png
COPY entrypoint.sh /app/entrypoint.sh

# Make scripts executable
RUN chmod +x /app/entrypoint.sh /app/postprocess.py

USER $UID

ENTRYPOINT ["/app/entrypoint.sh"]