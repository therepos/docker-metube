FROM alexta69/metube:latest

# Install Python, pip, ffmpeg, mutagen (Alpine compatible)
RUN apk add --no-cache python3 py3-pip ffmpeg && \
    pip3 install mutagen

# Copy the postprocessor and the cover image
COPY postprocess.py /postprocess/postprocess.py
COPY cover.png /postprocess/cover.png

RUN chmod +x /postprocess/postprocess.py
