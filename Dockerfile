FROM alexta69/metube:latest

# Install dependencies
RUN apk add --no-cache ffmpeg python3 py3-pip build-base libffi-dev

# Install Python packages
RUN pip install mutagen watchdog

# Copy custom files
COPY postprocess.py /app/postprocess.py
COPY cover.png /app/cover.png

# Set workdir
WORKDIR /app

# Optional: run postprocess on start (or trigger another way)
CMD ["python3", "postprocess.py"]
