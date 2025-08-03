FROM alexta69/metube:latest

# Install required tools
RUN apt-get update && \
    apt-get install -y python3-pip inotify-tools && \
    pip3 install mutagen && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add postprocess script and cover
COPY postprocess.py /app/postprocess.py
COPY cover.png /app/cover.png

# Run postprocess alongside MeTube
CMD bash -c "python3 /app/postprocess.py & exec /start.sh"
