FROM alexta69/metube:latest

# Install dependencies using Alpine package manager
RUN apk add --no-cache python3 py3-pip inotify-tools && \
    pip3 install mutagen

# Add postprocess script and cover
COPY postprocess.py /app/postprocess.py
COPY cover.png /app/cover.png

# Run postprocess alongside MeTube
CMD sh -c "python3 /app/postprocess.py & exec /start.sh"
