FROM alexta69/metube:latest

# Install dependencies using Alpine's apk
RUN apk add --no-cache python3 py3-pip ffmpeg && \
    pip3 install mutagen

# Add your postprocessing script
COPY postprocess.py /postprocess/postprocess.py
RUN chmod +x /postprocess/postprocess.py
