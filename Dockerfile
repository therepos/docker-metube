FROM alexta69/metube:latest

# Install Python and required packages
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Copy custom files
COPY postprocess.py /app/postprocess.py
COPY cover.png /app/cover.png
COPY entrypoint.sh /app/entrypoint.sh

# Make scripts executable
RUN chmod +x /app/entrypoint.sh /app/postprocess.py

# Switch back to the original user
USER $UID

# Use custom entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]