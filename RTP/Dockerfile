FROM python:3.11-slim

# Actualización: Usamos libgl1 en lugar de libgl1-mesa-glx
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalamos la versión "headless" de OpenCV que es ideal para Docker 
# porque no necesita interfaces gráficas (X11)
RUN pip install opencv-python-headless

COPY stream.py .

CMD ["python", "stream.py"]