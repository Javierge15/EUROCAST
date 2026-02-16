import cv2
import asyncio
import base64
import time
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

# Configuración de cámara (ajusta el índice según tu PC)
camera_path = "/dev/video3"

@app.get("/")
async def get():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    camera = cv2.VideoCapture(camera_path)
    frame_count = 0
    
    try:
        while True:
            success, frame = camera.read()
            if success:
                # 1. Procesamiento y Codificación
                frame = cv2.resize(frame, (640, 480))
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                # 2. Preparar Payload con Metadatos para el Paper
                payload = {
                    "f_id": frame_count,
                    "t_sent": time.time(),  # Timestamp de alta precisión
                    "image": f"data:image/jpeg;base64,{jpg_as_text}"
                }
                
                # 3. Enviar vía WebSocket
                await websocket.send_json(payload)
                frame_count += 1

            # Escuchar comandos de control (no bloqueante)
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=0.001)
            except asyncio.TimeoutError:
                pass
            
            # Control de Framerate (~30 FPS)
            await asyncio.sleep(0.033) 
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        camera.release()

if __name__ == "__main__":
    import uvicorn
    # Ejecuta con: python main.py
    uvicorn.run(app, host="0.0.0.0", port=8000)