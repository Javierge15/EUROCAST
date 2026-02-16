import cv2
import asyncio
import base64
import time
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from aiortc import RTCPeerConnection, RTCSessionDescription

app = FastAPI()
camera_path = "/dev/video0"

pcs = set()

@app.get("/")
async def get():
    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/offer")
async def offer(request: Request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])
    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState == "failed" or pc.connectionState == "closed":
            await pc.close()
            pcs.discard(pc)

    @pc.on("datachannel")
    def on_datachannel(channel):
        @channel.on("message")
        def on_message(message):
            data = json.loads(message)
            
            # --- LÓGICA DE SINCRONIZACIÓN ---
            if data.get("type") == "sync_request":
                channel.send(json.dumps({
                    "type": "sync_response",
                    "server_time": time.time(),
                    "client_t1": data["client_t1"]
                }))
                # Una vez sincronizado, empezamos el streaming
                asyncio.create_task(send_video_stream(channel))
            
            else:
                # Otros comandos de control
                pass

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return JSONResponse(
        content={"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
    )

async def send_video_stream(channel):
    camera = cv2.VideoCapture(camera_path)
    frame_count = 0
    try:
        while channel.readyState == "open":
            start_loop = time.time()
            success, frame = camera.read()
            if success:
                frame = cv2.resize(frame, (640, 480))
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                payload = {
                    "type": "video_frame", # Añadido para diferenciar
                    "f_id": frame_count,
                    "t_sent": time.time(),
                    "image": f"data:image/jpeg;base64,{jpg_as_text}"
                }
                channel.send(json.dumps(payload))
                frame_count += 1

            process_time = time.time() - start_loop
            await asyncio.sleep(max(0, 0.033 - process_time))
    except Exception as e:
        print(f"Error streaming: {e}")
    finally:
        camera.release()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)