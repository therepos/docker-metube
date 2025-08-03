FROM alexta69/metube:latest

# Install dependencies
RUN apt update && \
    apt install -y python3 python3-pip ffmpeg && \
    pip3 install mutagen && \
    rm -rf /var/lib/apt/lists/*

# Add the postprocessing script
COPY postprocess.py /postprocess/postprocess.py
RUN chmod +x /postprocess/postprocess.py
