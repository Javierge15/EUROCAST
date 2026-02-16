import cv2
import asyncio
import base64
import time
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

# Configuración de cámara (ajusta el índice según tu PC)
camera_path = "/dev/video0"

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
            # 1. Escuchar mensajes del cliente (Sincronización o Control)
            try:
                # Usamos receive_json para manejar los comandos de control y sync
                data = await asyncio.wait_for(websocket.receive_json(), timeout=0.005)
                
                # Lógica de sincronización de reloj
                if data.get("type") == "sync_request":
                    await websocket.send_json({
                        "type": "sync_response",
                        "server_time": time.time(),
                        "client_t1": data["client_t1"]
                    })
            except (asyncio.TimeoutError, json.JSONDecodeError):
                pass

            # 2. Captura y envío de video
            success, frame = camera.read()
            if success:
                frame = cv2.resize(frame, (640, 480))
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                payload = {
                    "type": "video_frame",
                    "f_id": frame_count,
                    "t_sent": time.time(),
                    "image": f"data:image/jpeg;base64,{jpg_as_text}"
                }
                
                await websocket.send_json(payload)
                frame_count += 1

            await asyncio.sleep(0.033) # ~30 FPS
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        camera.release()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)