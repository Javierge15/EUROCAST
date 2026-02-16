import cv2
import asyncio
import base64
import time
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from aiortc import RTCPeerConnection, RTCSessionDescription

app = FastAPI()
camera_path = "/dev/video3"

# Almacén de conexiones activas
pcs = set()

@app.get("/")
async def get():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

# --- LÓGICA DE SIGNALING (Intercambio de SDP) ---
@app.post("/offer")
async def offer(request: Request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    # Manejar cierre de conexión
    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState == "failed" or pc.connectionState == "closed":
            await pc.close()
            pcs.discard(pc)

    # Cuando el cliente abre un canal de datos
    @pc.on("datachannel")
    def on_datachannel(channel):
        if channel.label == "telemetry_stream":
            asyncio.create_task(send_video_stream(channel))
        
        @channel.on("message")
        def on_message(message):
            # Recibir comandos de control (Steering/Brake)
            print(f"Comando WebRTC recibido: {message}")

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return JSONResponse(
        content={"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    )

# --- LOOP DE ENVÍO DE VIDEO ---
async def send_video_stream(channel):
    camera = cv2.VideoCapture(camera_path)
    frame_count = 0
    
    try:
        while channel.readyState == "open":
            start_loop = time.time()
            success, frame = camera.read()
            
            if success:
                frame = cv2.resize(frame, (640, 480))
                # Calidad 70% JPEG
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                # Mismo payload que en WebSockets para comparar peras con peras
                payload = {
                    "f_id": frame_count,
                    "t_sent": time.time(),
                    "image": f"data:image/jpeg;base64,{jpg_as_text}"
                }
                
                try:
                    # En WebRTC DataChannel hay limite de tamaño (64kb default)
                    # pero aiortc maneja mensajes grandes mejor que el browser a veces.
                    # Si falla, baja la calidad del JPG o la resolución.
                    channel.send(json.dumps(payload))
                    frame_count += 1
                except Exception as e:
                    print(f"Frame drop o buffer lleno: {e}")

            # Control de FPS (~30fps)
            process_time = time.time() - start_loop
            await asyncio.sleep(max(0, 0.033 - process_time))
            
    except Exception as e:
        print(f"Error streaming: {e}")
    finally:
        camera.release()

if __name__ == "__main__":
    import uvicorn
    # Importante: WebRTC usa puertos UDP dinámicos, host network es ideal
    uvicorn.run(app, host="0.0.0.0", port=8000)