FROM python:3.10-slim

# Actualizamos a librerías más modernas de OpenGL
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos primero los requerimientos para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir fastapi uvicorn opencv-python-headless websockets

COPY ./app .

CMD ["python", "main.py"]