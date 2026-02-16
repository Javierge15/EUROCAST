FROM python:3.10-slim

# Instalamos dependencias para aiortc (PyAV) y OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libavdevice-dev \
    libavfilter-dev \
    libopus-dev \
    libvpx-dev \
    pkg-config \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Actualizamos pip e instalamos dependencias
# (Modificado para incluir aiortc)
RUN pip install --upgrade pip
RUN pip install --no-cache-dir fastapi uvicorn opencv-python-headless aiortc aiohttp

COPY ./app .

CMD ["python", "main.py"]