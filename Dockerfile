FROM alexta69/metube:latest

# Install Python, pip, ffmpeg, mutagen
RUN apk add --no-cache python3 py3-pip ffmpeg && \
    pip3 install mutagen

# Copy everything needed for postprocessing
COPY postprocess.py /postprocess/postprocess.py
COPY cover.png /postprocess/cover.png
COPY entrypoint.sh /entrypoint.sh

# Make sure scripts are executable
RUN chmod +x /postprocess/postprocess.py /entrypoint.sh

# Use our custom wrapper as entrypoint
ENTRYPOINT ["/entrypoint.sh"]
