# Base Image
FROM python:3.10-slim

# Working Directory
WORKDIR /app

# System Dependencies (OpenCV, Audio)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    portaudio19-dev \
    python3-pyaudio \
    && rm -rf /var/lib/apt/lists/*

# Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Application Code
COPY . .

# Environment Variables (Defaults)
ENV SYSTEM_MODE=remote
ENV PYTHONUNBUFFERED=1
# ENV ADK_RELAY_URL=wss://your-relay-server.com (configure in Coolify)

# Entrypoint
# Entrypoint
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
